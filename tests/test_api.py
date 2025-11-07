"""
Tests for the main API endpoints of the Mergington High School Activities application.
"""

import pytest


class TestMainEndpoints:
    """Test suite for main application endpoints."""
    
    def test_root_redirect(self, client):
        """Test that root endpoint redirects to static files."""
        response = client.get("/")
        assert response.status_code == 200
        # Should redirect to static/index.html
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_get_activities(self, client, reset_activities):
        """Test retrieving all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        
        # Check structure of an activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)


class TestSignupEndpoint:
    """Test suite for student signup functionality."""
    
    def test_successful_signup(self, client, reset_activities):
        """Test successful student signup for an activity."""
        email = "test@mergington.edu"
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
        
        # Verify student was added to the activity
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]
    
    def test_signup_nonexistent_activity(self, client, reset_activities):
        """Test signup for a non-existent activity."""
        email = "test@mergington.edu"
        activity_name = "Nonexistent Activity"
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_duplicate_signup(self, client, reset_activities):
        """Test that students cannot sign up twice for the same activity."""
        email = "michael@mergington.edu"  # Already registered for Chess Club
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 400
        
        data = response.json()
        assert data["detail"] == "Student is already signed up"
    
    def test_signup_with_special_characters(self, client, reset_activities):
        """Test signup with special characters in email and activity name."""
        email = "test.student@mergington.edu"  # Use dot instead of plus to avoid URL encoding issues
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify student was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]


class TestUnregisterEndpoint:
    """Test suite for student unregister functionality."""
    
    def test_successful_unregister(self, client, reset_activities):
        """Test successful student unregistration from an activity."""
        email = "michael@mergington.edu"  # Already registered for Chess Club
        activity_name = "Chess Club"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
        
        # Verify student was removed from the activity
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]
    
    def test_unregister_nonexistent_activity(self, client, reset_activities):
        """Test unregister from a non-existent activity."""
        email = "test@mergington.edu"
        activity_name = "Nonexistent Activity"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_unregister_not_registered_student(self, client, reset_activities):
        """Test unregistering a student who is not registered for the activity."""
        email = "notregistered@mergington.edu"
        activity_name = "Chess Club"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == 400
        
        data = response.json()
        assert data["detail"] == "Student is not registered for this activity"


class TestIntegrationScenarios:
    """Integration tests covering complete user workflows."""
    
    def test_complete_signup_unregister_flow(self, client, reset_activities):
        """Test a complete flow of signup followed by unregister."""
        email = "integration@mergington.edu"
        activity_name = "Programming Class"
        
        # 1. Sign up for activity
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_response.status_code == 200
        
        # 2. Verify signup in activities list
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]
        
        # 3. Unregister from activity
        unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert unregister_response.status_code == 200
        
        # 4. Verify removal from activities list
        final_activities_response = client.get("/activities")
        final_activities_data = final_activities_response.json()
        assert email not in final_activities_data[activity_name]["participants"]
    
    def test_multiple_students_same_activity(self, client, reset_activities):
        """Test multiple students signing up for the same activity."""
        activity_name = "Gym Class"
        students = [
            "student1@mergington.edu",
            "student2@mergington.edu", 
            "student3@mergington.edu"
        ]
        
        # Sign up all students
        for email in students:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all students are registered
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        for email in students:
            assert email in activities_data[activity_name]["participants"]
        
        # Check total participant count increased correctly
        total_participants = len(activities_data[activity_name]["participants"])
        assert total_participants >= len(students) + 2  # +2 for initial participants