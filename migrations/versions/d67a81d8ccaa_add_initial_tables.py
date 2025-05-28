"""Add initial tables

Revision ID: d67a81d8ccaa
Revises: 
Create Date: 2025-05-28 23:43:56.875022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd67a81d8ccaa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    # Create 'properties' table
    op.create_table(
        'properties',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('property_name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('property_type', sa.String(length=50), nullable=False),
        sa.Column('bhk_type', sa.String(length=10), nullable=False),
        sa.Column('bathrooms', sa.Integer(), nullable=False),
        sa.Column('area_sqft', sa.Float(), nullable=False),
        sa.Column('rent_price', sa.Float(), nullable=False),
        sa.Column('deposit', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['rms.locations.id']),
        sa.ForeignKeyConstraint(['owner_id'], ['rms.users.id']),
        schema='rms'
    )

    # Create 'locations' table
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=False, unique=True),
        sa.Column('street', sa.String(length=255), nullable=False),
        sa.Column('locality', sa.String(length=100), nullable=False),
        sa.Column('near_by', sa.String(length=255), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('district', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=100), nullable=False),
        sa.Column('zipcode', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['rms.properties.id']),
        schema='rms'
    )

    # Create 'users' table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('first_name', sa.String(length=50), nullable=False),
        sa.Column('last_name', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=50), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.Column('identity_verified', sa.Boolean(), nullable=True),
        sa.Column('profile_image', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        schema='rms'
    )

     

    op.create_foreign_key(
        'fk_properties_location_id_locations',
        'properties', 'locations',
        ['location_id'], ['id'],
        source_schema='rms',
        referent_schema='rms'
    )


    # Create 'roles' table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        schema='rms'
    )

    

    # Create unique indexes on 'users.email' and 'users.phone'
    with op.batch_alter_table('users', schema='rms') as batch_op:
        batch_op.create_index('ix_rms_users_email', ['email'], unique=True)
        batch_op.create_index('ix_rms_users_phone', ['phone'], unique=True)

    # Create 'property_images' table
    op.create_table(
        'property_images',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('image_url', sa.String(length=512), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['rms.properties.id']),
        schema='rms'
    )

    # Create 'user_roles' table (association table for many-to-many relation)
    op.create_table(
        'user_roles',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['rms.users.id']),
        sa.ForeignKeyConstraint(['role_id'], ['rms.roles.id']),
        sa.PrimaryKeyConstraint('user_id', 'role_id'),
        schema='rms'
    )


def downgrade():
    # Drop tables in reverse order to respect foreign key constraints
    op.drop_table('user_roles', schema='rms')
    op.drop_table('property_images', schema='rms')

    with op.batch_alter_table('users', schema='rms') as batch_op:
        batch_op.drop_index('ix_rms_users_phone')
        batch_op.drop_index('ix_rms_users_email')

    op.drop_table('users', schema='rms')
    op.drop_table('roles', schema='rms')
    op.drop_table('properties', schema='rms')
    op.drop_table('locations', schema='rms')
