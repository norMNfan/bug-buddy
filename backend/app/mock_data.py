from .database import SessionLocal
from .models import Switch


def init_mock_data():
    db = SessionLocal()

    # Check if we already have data
    if db.query(Switch).first() is None:
        # Create mock switches
        mock_switches = [
            Switch(
                id="switch1",
                user_email="user1@example.com",
                name="Living Room Light",
                content="ON",
            ),
            Switch(
                id="switch2",
                user_email="user1@example.com",
                name="Kitchen Light",
                content="OFF",
            ),
            Switch(
                id="switch3",
                user_email="user2@example.com",
                name="Bedroom Light",
                content="ON",
            ),
        ]

        # Add all switches to database
        for switch in mock_switches:
            db.add(switch)

        db.commit()

    db.close()
