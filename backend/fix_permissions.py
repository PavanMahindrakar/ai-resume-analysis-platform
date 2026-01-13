"""
Script to fix PostgreSQL permissions for ai_resume_user.
Run this script to grant necessary permissions to the database user.
"""
import psycopg2
from psycopg2 import sql
import getpass

# Database connection details - you'll need to provide superuser credentials
print("=" * 60)
print("PostgreSQL Permission Fix Script")
print("=" * 60)
print("\nThis script will grant necessary permissions to ai_resume_user")
print("You need to provide PostgreSQL superuser credentials (usually 'postgres')\n")

# Get superuser credentials
superuser = input("PostgreSQL superuser (default: postgres): ").strip() or "postgres"
superuser_password = getpass.getpass(f"Password for {superuser}: ")
host = input("Host (default: localhost): ").strip() or "localhost"
port = input("Port (default: 5432): ").strip() or "5432"
database = "ai_resume_intelligence"

try:
    # Connect as superuser
    print(f"\nConnecting to PostgreSQL as {superuser}...")
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=superuser,
        password=superuser_password
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("Connected successfully!\n")
    
    # Grant permissions
    print("Granting permissions to ai_resume_user...")
    
    permissions = [
        "GRANT USAGE ON SCHEMA public TO ai_resume_user",
        "GRANT CREATE ON SCHEMA public TO ai_resume_user",
        "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ai_resume_user",
        "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ai_resume_user",
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ai_resume_user",
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ai_resume_user",
    ]
    
    for permission in permissions:
        try:
            cursor.execute(permission)
            print(f"✓ {permission}")
        except Exception as e:
            print(f"✗ {permission}")
            print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("Permissions granted successfully!")
    print("=" * 60)
    print("\nYou can now run: alembic upgrade head")
    
    cursor.close()
    conn.close()
    
except psycopg2.OperationalError as e:
    print(f"\n✗ Connection failed: {e}")
    print("\nPlease check:")
    print("1. PostgreSQL is running")
    print("2. Database 'ai_resume_intelligence' exists")
    print("3. Superuser credentials are correct")
    print("4. Host and port are correct")
except Exception as e:
    print(f"\n✗ Error: {e}")
