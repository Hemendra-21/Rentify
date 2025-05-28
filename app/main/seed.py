from app.main.extensions import db
from app.main.models.role import Role

def seed_roles():
    roles_to_seed = ['tenant', 'landlord', 'admin']
    for role_name in roles_to_seed:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            new_role = Role(name=role_name)
            db.session.add(new_role)
            print(f"Added role: {role_name}")
    db.session.commit()
    print("Role seeding complete.")
