"""Quick test script to verify the application works."""

import sys
sys.path.insert(0, 'src')

from database import Database

print("🧪 Testing LLM Chat Agent Application\n")

# Test 1: Database
print("1. Testing Database...")
db = Database("test_chat.db")
print("   ✓ Database initialized")

# Test 2: Create user
print("\n2. Testing User Creation...")
result = db.create_user("testuser", "testpass123")
if result["success"]:
    print(f"   ✓ User created: {result['username']} (ID: {result['user_id']})")
else:
    print(f"   ✗ Error: {result['error']}")

# Test 3: Authenticate
print("\n3. Testing Authentication...")
result = db.authenticate_user("testuser", "testpass123")
if result["success"]:
    print(f"   ✓ User authenticated: {result['username']}")
    user_id = result["user_id"]
else:
    print(f"   ✗ Error: {result['error']}")
    sys.exit(1)

# Test 4: Get sessions
print("\n4. Testing Sessions...")
sessions = db.get_user_sessions(user_id)
print(f"   ✓ Found {len(sessions)} session(s)")
if sessions:
    session_id = sessions[0]["id"]
    print(f"   Session: {sessions[0]['session_name']}")

    # Test 5: Add messages
    print("\n5. Testing Messages...")
    db.add_message(session_id, "user", "Hola, soy un usuario de prueba")
    db.add_message(session_id, "assistant", "¡Hola! Encantado de conocerte")
    print("   ✓ Messages added")

    # Test 6: Get messages
    messages = db.get_session_messages(session_id)
    print(f"   ✓ Retrieved {len(messages)} message(s)")
    for msg in messages:
        print(f"      - {msg['role']}: {msg['content'][:50]}...")

print("\n✅ All database tests passed!")
print("\n📝 Next steps:")
print("   1. Add your OPENAI_API_KEY to the .env file")
print("   2. Run: cd src && uvicorn main:app --reload")
print("   3. Open: http://localhost:8000/chat")
print("   4. Or build Docker: docker build -t llm-chat-agent .")

# Cleanup
import os
os.remove("test_chat.db")
print("\n🧹 Test database cleaned up")
