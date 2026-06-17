# DevDiary API

REST API for diary entries. JSON in, JSON out. All entry endpoints are **per-user** —
you only ever see and touch your own entries.

## Base URLs

| Environment | URL |
|---|---|
| Production (Render) | `https://devdiary-qf1x.onrender.com` |
| Local | `http://localhost:8000` |

## Postman setup

Create an **Environment** with these variables, then use `{{base_url}}` / `{{token}}` in requests:

| Variable | Initial value |
|---|---|
| `base_url` | `https://devdiary-qf1x.onrender.com` |
| `token` | *(leave blank — fill after register/login)* |

**Authentication:** every endpoint except `register` and `token` needs this header:

```
Authorization: Token {{token}}
```

> Tip: on the **Register** and **Get token** requests, add this to the **Tests** tab to auto-save the token:
> ```javascript
> pm.environment.set("token", pm.response.json().token);
> ```

---

## 1. Register a new account

Create a user and get a token back in one call. No auth required.

```
POST {{base_url}}/api/register/
Content-Type: application/json
```
```json
{
  "username": "alice",
  "password": "s3cure-pw-9000",
  "email": "alice@example.com"
}
```

- `email` is optional.
- `password` must pass Django's validators (min length, not all-numeric, not too common).

**201 Created**
```json
{ "id": 7, "username": "alice", "token": "9c8f0e3b2a1d4f5e6a7b8c9d0e1f2a3b4c5d6e7f" }
```
**400** if the username is taken or the password is weak (errors per field).

---

## 2. Get a token (existing user)

For a user that already exists (e.g. created via the website signup).

```
POST {{base_url}}/api/token/
Content-Type: application/json
```
```json
{ "username": "alice", "password": "s3cure-pw-9000" }
```

**200 OK**
```json
{ "token": "9c8f0e3b2a1d4f5e6a7b8c9d0e1f2a3b4c5d6e7f" }
```

---

## 3. List entries

```
GET {{base_url}}/api/entries/
Authorization: Token {{token}}
```

Returns **paginated** results (10 per page):

**200 OK**
```json
{
  "count": 23,
  "next": "https://devdiary-qf1x.onrender.com/api/entries/?page=2",
  "previous": null,
  "results": [
    {
      "id": 12,
      "author": "alice",
      "topic": "Learned Django signals",
      "minutes": 45,
      "mood": "+",
      "notes": "finally clicked",
      "created_at": "2026-06-29T21:14:03.512Z"
    }
  ]
}
```

### Query parameters (combine freely)

| Param | Example | Meaning |
|---|---|---|
| `page` | `?page=2` | page number |
| `mood` | `?mood=%2B` | filter by mood (see note) |
| `search` | `?search=django` | text match in `topic` + `notes` |
| `ordering` | `?ordering=-minutes` | sort by `minutes` or `created_at` (`-` = descending) |

> **mood `+` gotcha:** a literal `+` in a URL means "space". To filter good-mood entries,
> URL-encode it as `%2B` → `?mood=%2B`. In Postman's Params tab, just type `+` as the value
> and it encodes it for you. Values: `+` good, `=` ok, `-` bad.

Combined example:
```
GET {{base_url}}/api/entries/?search=django&ordering=-minutes&page=1
```

---

## 4. Create an entry

```
POST {{base_url}}/api/entries/
Authorization: Token {{token}}
Content-Type: application/json
```
```json
{
  "topic": "Read about Redis caching",
  "minutes": 30,
  "mood": "=",
  "notes": "optional free text"
}
```

- `topic` (≤100 chars) and `minutes` (positive integer) are **required**.
- `mood` optional, defaults to `=`. One of `+`, `=`, `-`.
- `notes` optional.
- `author` is set automatically from your token — you can't send it.

**201 Created** → the new entry object (same shape as in the list).

---

## 5. Get one entry

```
GET {{base_url}}/api/entries/{id}/
Authorization: Token {{token}}
```
**200 OK** → the entry. **404** if it doesn't exist *or* isn't yours.

---

## 6. Update an entry (full)

Replaces all writable fields.

```
PUT {{base_url}}/api/entries/{id}/
Authorization: Token {{token}}
Content-Type: application/json
```
```json
{ "topic": "Updated topic", "minutes": 60, "mood": "+", "notes": "" }
```
**200 OK** → the updated entry.

---

## 7. Update an entry (partial)

Send only the fields you want to change.

```
PATCH {{base_url}}/api/entries/{id}/
Authorization: Token {{token}}
Content-Type: application/json
```
```json
{ "minutes": 90 }
```
**200 OK** → the updated entry.

---

## 8. Delete an entry

```
DELETE {{base_url}}/api/entries/{id}/
Authorization: Token {{token}}
```
**204 No Content** (empty body). **404** if not yours.

---

## 9. API root (browsable)

```
GET {{base_url}}/api/
Authorization: Token {{token}}
```
Lists the available endpoints. Open it in a browser (while logged into the site) for DRF's
clickable browsable API.

---

## Entry object fields

| Field | Type | Writable | Notes |
|---|---|---|---|
| `id` | int | no | |
| `author` | string | no | the owner's username |
| `topic` | string | yes | ≤ 100 chars, required |
| `minutes` | int | yes | positive integer, required |
| `mood` | string | yes | `+` good / `=` ok / `-` bad (default `=`) |
| `notes` | string | yes | optional free text |
| `created_at` | datetime | no | ISO 8601, set on creation |

## Status codes & limits

- **401 Unauthorized** — missing/invalid token (or expired session).
- **400 Bad Request** — validation error (body has per-field messages).
- **404 Not Found** — entry doesn't exist or belongs to another user.
- **429 Too Many Requests** — rate limit hit. Limits: anonymous **20/hour**, authenticated **1000/day**.
