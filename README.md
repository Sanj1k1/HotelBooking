
## Team Members
| Name             | ID          |
|-----------------|------------|
| Amirgali Sanzhar | 22B030621 |
| Turganbek Nurzat | 22B030604 |
| Zhanshin  Arsen  | 22B031249 |

---
## Project Description
HotelBooking is a web application for hotel reservations. Users can browse available hotels, make bookings, and administrators can manage users and hotels. 
The platform also provides APIs for frontend or mobile app integration.

---
## Installation and Running Locally

1. Clone the repository:
```bash
git clone <repo-url>
```
2. Navigate to the project folder:
```bash
cd HotelBooking
```
3. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```
4. Install dependencies:
```bash
pip install -r requirements/prod.txt
```
5. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Run the server:
```bash
python manage.py runserver
```

## API Documentation
API documentation is available at /api/docs/ if using DRF Spectacular / Swagger / Redoc.

---
## Running Tests
```bash
pytest -v 
```
