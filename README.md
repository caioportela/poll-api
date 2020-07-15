# poll-api

<!-- toc -->
- [Installation](#installation)
- [Usage](#usage)
  - [Create a poll](#post-poll)
  - [Find a poll](#get-pollpoll_id)
  - [Vote option](#post-polloption_idvote)
  - [Check poll stats](#get-pollpoll_idstats)
- [Test](#test)
<!-- tocstop -->

## Installation

Unzip the `poll-api.zip` file

```bash
$ cd poll-api
$ pip install -r requirements.txt
```

## Usage

Before run the application, export the environment variable

```bash
$ export FLASK_APP=api
```

and initialize the database

```bash
$ flask init_db
```

then run

```bash
$ flask run
```

The application is now running on `http://127.0.0.1:5000/`.

-------------------------------------------------------------------------------

Requesting the API through cURL:

### `POST /poll`
Creates a poll

- Headers
  - `Content-Type: application/json`

- Body
  ```json
  {
    "poll_description": "This is the question",
    "options": [
      "First Option",
      "Second Option",
      "Third Option"
    ]
  }
  ```

- Request
  ```bash
  $ curl -X POST http://127.0.0.1:5000/poll -H 'Content-Type:application/json' -d '{"poll_description":"This is the question","options":["First Option","Second Option","Third Option"]}'
  ```

- Response
  ```json
  {
    "poll_id": 1
  }
  ```
-------------------------------------------------------------------------------

### `GET /poll/:poll_id`
Returns poll information

- Request
  ```bash
  $ curl http://127.0.0.1:5000/poll/1
  ```

- Response
  ```json
  {
    "poll_id": 1,
    "poll_description": "This is the question",
    "options": [
      {
        "option_id": 1,
        "option_description": "First Option"
      },
      {
        "option_id": 2,
        "option_description": "Second Option"
      },
      {
        "option_id": 3,
        "option_description": "Third Option"
      }
    ]
  }
  ```

-------------------------------------------------------------------------------

### `POST /poll/:option_id/vote`
Computes a vote for the option

- Request
  ```bash
  $ curl -X POST http://127.0.0.1:5000/poll/2/vote
  ```

- Response
  ```json
  {
    "option_id": 2
  }
  ```

-------------------------------------------------------------------------------

### `GET /poll/:poll_id/stats`
Returns poll stats

- Request
  ```bash
  $ curl http://127.0.0.1:5000/poll/1/stats
  ```

- Response
  ```json
  {
    "views": 3,
    "votes": [
      {
        "option_id": 1,
        "qty": 1
      },
      {
        "option_id": 2,
        "qty": 0
      },
      {
        "option_id": 3,
        "qty": 0
      }
    ]
  }
  ```

-------------------------------------------------------------------------------

## Test

To run tests simply run:
```bash
$ pytest
```

For code coverage:
```bash
$ pytest --cov=api
```
