"""
Tests for data validation and edge cases.
"""

import pytest


class TestDataValidation:
    """Test suite for data validation and edge cases."""
    
    def test_empty_email_signup(self, client, reset_activities):
        """Test signup with empty email parameter."""
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup?email=")
        # Should still work as FastAPI accepts empty strings
        assert response.status_code == 200
    
    def test_url_encoded_activity_names(self, client, reset_activities):
        """Test activities with spaces in names are properly URL encoded."""
        email = "test@mergington.edu"
        activity_name = "Chess Club"  # Contains space
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
    
    def test_case_sensitive_activity_names(self, client, reset_activities):
        """Test that activity names are case sensitive."""
        email = "test@mergington.edu"
        
        # Correct case
        response1 = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response1.status_code == 200
        
        # Reset for next test
        client.delete(f"/activities/Chess Club/unregister?email={email}")
        
        # Wrong case
        response2 = client.post(f"/activities/chess club/signup?email={email}")
        assert response2.status_code == 404


class TestErrorHandling:
    """Test suite for error handling scenarios."""
    
    def test_malformed_request_missing_email(self, client):
        """Test request without email parameter."""
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup")
        # FastAPI will return 422 for missing required query parameter
        assert response.status_code == 422
    
    def test_invalid_http_methods(self, client):
        """Test using invalid HTTP methods on endpoints."""
        # GET on signup endpoint
        response1 = client.get("/activities/Chess Club/signup?email=test@mergington.edu")
        assert response1.status_code == 405  # Method Not Allowed
        
        # POST on unregister endpoint  
        response2 = client.post("/activities/Chess Club/unregister?email=test@mergington.edu")
        assert response2.status_code == 405  # Method Not Allowed


class TestBoundaryConditions:
    """Test suite for boundary conditions and limits."""
    
    def test_very_long_email(self, client, reset_activities):
        """Test signup with very long email address."""
        long_email = "a" * 100 + "@mergington.edu"
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup?email={long_email}")
        assert response.status_code == 200
        
        # Verify it was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert long_email in activities_data[activity_name]["participants"]
    
    def test_special_characters_in_email(self, client, reset_activities):
        """Test signup with special characters in email."""
        special_emails = [
            "test.name@mergington.edu", 
            "test_underscore@mergington.edu",
            "test-dash@mergington.edu"
        ]
        
        activity_name = "Programming Class"
        
        for email in special_emails:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == 200
            
            # Verify it was added
            activities_response = client.get("/activities")
            activities_data = activities_response.json()
            assert email in activities_data[activity_name]["participants"]
    
    def test_url_encoding_behavior(self, client, reset_activities):
        """Test URL encoding behavior with plus signs in email."""
        import urllib.parse
        
        activity_name = "Chess Club"
        # Plus signs in URLs are decoded as spaces - this is expected behavior
        raw_email = "test+tag@mergington.edu"
        encoded_email = urllib.parse.quote_plus(raw_email)
        
        response = client.post(f"/activities/{activity_name}/signup?email={encoded_email}")
        assert response.status_code == 200
        
        # Verify the properly encoded email was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert raw_email in activities_data[activity_name]["participants"]