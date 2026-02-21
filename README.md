# Image Processing API

A FastAPI-based backend service for uploading images, extracting metadata, generating thumbnails, and storing records in a SQLite database.

---

## Features

- Upload JPG and PNG images
- Automatic metadata extraction (width, height, format, size)
- Thumbnail generation:
  - Small (128x128)
  - Medium (512x512)
- SQLite database persistence
- RESTful API
- Interactive Swagger documentation

---

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pillow
- Uvicorn

---

## Project Structure

```
image-processing-api/
│
├── app/
|   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── database.py
│
├── uploads/
├── thumbnails/
├── requirements.txt
└── README.md
```

---

## Run Locally

### Clone the repository

```bash
git clone https://github.com/Random-Leg/image-processing-api
cd image-processing-api
```

### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the server

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

Once running, open:

```
http://127.0.0.1:8000/docs
```

Swagger UI will be available.

---

## Author

Built as a backend project using FastAPI.