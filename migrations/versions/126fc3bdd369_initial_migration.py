"""Initial migration

Revision ID: 126fc3bdd369
Revises: 
Create Date: 2023-01-05 01:23:18.215878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '126fc3bdd369'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kaggle_d1_fraud_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('signup_time', sa.DateTime(), nullable=True),
    sa.Column('purchase_time', sa.DateTime(), nullable=True),
    sa.Column('purchase_value', sa.Float(), nullable=True),
    sa.Column('device_id', sa.String(length=20), nullable=True),
    sa.Column('source', sa.String(length=3), nullable=True),
    sa.Column('browser', sa.String(length=10), nullable=True),
    sa.Column('sex', sa.String(length=1), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('ip_address', sa.Float(), nullable=True),
    sa.Column('is_fraud', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('kaggle_d1_fraud_data', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_kaggle_d1_fraud_data_device_id'), ['device_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d1_fraud_data_ip_address'), ['ip_address'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d1_fraud_data_signup_time'), ['signup_time'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d1_fraud_data_source'), ['source'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d1_fraud_data_user_id'), ['user_id'], unique=False)

    op.create_table('kaggle_d1_ipaddress_to_country',
    sa.Column('lb_ip_address', sa.BIGINT(), nullable=False),
    sa.Column('ub_ip_address', sa.BIGINT(), nullable=False),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('lb_ip_address', 'ub_ip_address')
    )
    op.create_table('kaggle_d2_onlinefraud',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('step', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('name_orig', sa.String(length=50), nullable=True),
    sa.Column('oldbalance_org', sa.Float(), nullable=True),
    sa.Column('newbalance_org', sa.Float(), nullable=True),
    sa.Column('name_dest', sa.String(length=50), nullable=True),
    sa.Column('oldbalance_dest', sa.Float(), nullable=True),
    sa.Column('newbalance_dest', sa.Float(), nullable=True),
    sa.Column('is_fraud', sa.Boolean(), nullable=True),
    sa.Column('is_flagged_fraud', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('kaggle_d2_onlinefraud', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_kaggle_d2_onlinefraud_is_fraud'), ['is_fraud'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d2_onlinefraud_name_dest'), ['name_dest'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d2_onlinefraud_name_orig'), ['name_orig'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d2_onlinefraud_newbalance_dest'), ['newbalance_dest'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d2_onlinefraud_newbalance_org'), ['newbalance_org'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d2_onlinefraud_oldbalance_dest'), ['oldbalance_dest'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d2_onlinefraud_oldbalance_org'), ['oldbalance_org'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d2_onlinefraud_step'), ['step'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_d2_onlinefraud_type'), ['type'], unique=False)

    op.create_table('kaggle_meta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=75), nullable=False),
    sa.Column('value', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'name')
    )
    with op.batch_alter_table('kaggle_meta', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_kaggle_meta_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_kaggle_meta_value'), ['value'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('kaggle_meta', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_kaggle_meta_value'))
        batch_op.drop_index(batch_op.f('ix_kaggle_meta_name'))

    op.drop_table('kaggle_meta')
    with op.batch_alter_table('kaggle_d2_onlinefraud', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_kaggle_d2_onlinefraud_type'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d2_onlinefraud_step'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d2_onlinefraud_oldbalance_org'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d2_onlinefraud_oldbalance_dest'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d2_onlinefraud_newbalance_org'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d2_onlinefraud_newbalance_dest'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d2_onlinefraud_name_orig'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d2_onlinefraud_name_dest'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d2_onlinefraud_is_fraud'))

    op.drop_table('kaggle_d2_onlinefraud')
    op.drop_table('kaggle_d1_ipaddress_to_country')
    with op.batch_alter_table('kaggle_d1_fraud_data', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_kaggle_d1_fraud_data_user_id'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d1_fraud_data_source'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d1_fraud_data_signup_time'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d1_fraud_data_ip_address'))
        batch_op.drop_index(batch_op.f('ix_kaggle_d1_fraud_data_device_id'))

    op.drop_table('kaggle_d1_fraud_data')
    # ### end Alembic commands ###
