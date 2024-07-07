from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from user_gcp import models, schemas, crud
from user_gcp.database import SessionLocal, engine
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to create a new user
@app.post("/users/", tags=["Users"], response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# Endpoint to retrieve all users
@app.get("/users/", tags=["Users"], response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# Endpoint to update a user by ID
@app.patch("/users/{user_id}", tags=["Users"], response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, user=user)


# Endpoint to delete a user by ID
@app.delete("/users/{user_id}", tags=["Users"], response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db=db, user_id=user_id)


@app.post("/send_invite", tags=["Send mail"])
def send_invite():
    sender_email = "harikrishnansr1007@gmail.com"
    recipients = ["shraddha@aviato.consulting", "pooja@aviato.consulting"]
    subject = "API Documentation Invitation"
    body = """
    <html>
    <body>
        <div
            style="width: 600px; margin: auto; padding: 20px; font-family: Arial, sans-serif; background-color: #f4f4f4; border: 1px solid #ddd;">
            <h1
                style="background-color: #3971e0; color: white; padding: 10px 0; text-align: center;">API
                Documentation Invitation</h1>
            <p>Hello,</p>
            <p>I have excited to invite you to view my User Management API
                documentation on <strong>ReDoc</strong>.</p>
            <p>You can access the documentation by clicking the button
                below:</p>
            <a href="https://crud-user-428512.el.r.appspot.com/redoc"
                style="display: inline-block; padding: 10px 20px; color: white; background-color: #3971e0; text-decoration: none; border-radius: 5px;">View
                API Documentation</a>
            <p>As per the requirements, I have set up the API to handle user
                management for three different projects. The API supports the
                following operations:</p>
            <ul>
                <li>Create User</li>
                <li>Get User Details</li>
                <li>Update User Details</li>
                <li>Delete User</li>
            </ul>
            <p>I have also set up a GCP free tier account for deployment and GCP
                Postgres for the database.</p>
            <p>I have appreciate your time and look forward to your
                feedback.</p>
            <div
                style="width: 500px;background-color: #3971e0; margin: auto; padding: 20px; font-family: Arial, sans-serif; backgro border: 1px solid #ddd; color:white;text-align:center;">
                <p style="font-size:13px;">Thank you,</p>
                <p style="font-size:12px;">Harikrishnan</p>
                <p style=" font-size: 12px;">If you have any questions, feel
                    free to reply to this <a href="mailto:harikrishnansr007@gmail.com">harikrishnansr007@gmail.com</a>.</p>
            </div>
        </div>
    </body>
</html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, "wmarvfcyfjzvrmvh")
            server.sendmail(sender_email, recipients, msg.as_string())
        return {"message": "Invitation email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
