from typing import List, Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from tools.weather import get_5day_forecast
from tools.places import get_nearby_places
from tools.whatsapp import open_whatsapp
from tools.todo import add_task, list_tasks, update_task, delete_task
from tools.email_tool import get_important_emails
app = FastMCP()


@app.tool()
def check_important_emails(
    limit: Optional[int] = None,
    days: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    labels: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Scan Gmail for important messages over flexible time or label filters,
    including any raw attachments and parsed .ics meeting-invite details.

    Args:
      limit        (int?, default=None)   – max number of emails to fetch
      days         (int?, default=None)   – look back N days (e.g. 2 for today+1 prior)
      start_date   (str?, default=None)   – ISO date “YYYY-MM-DD” to begin range
      end_date     (str?, default=None)   – ISO date “YYYY-MM-DD” to end range
      labels       (List[str]?, default=None) – Gmail labels/folders to include

    Returns: List of dicts, each with keys:
      • categories         List[str]    – which of [“meeting”,“verification”,“job”,“subscription”,“delivery”]
      • subject            str
      • from               str          – the From: header
      • datetime           str (ISO)
      • body               str          – plain-text body
      • has_attachments    bool
      • attachments        List[{
            content_type: str,
            filename:     str,
            content:      str     # base-64/text/hex-decoded payload
        }]
      • links              List[str]    – all HTTP/HTTPS URLs in subject+body
      • tracking_numbers   List[str]    – any 7+ digit sequences
      • meeting_details    List[{
            organizer_cn: str,    # from the ICS
            meeting_url:  str,    # folded Teams URL
            location:     str,
            summary:      str,
            description:  str,
            meeting_start:      str,    # “YYYYMMDDTHHMMSS” This is the start time of the meeting
            meeting_end:        str,    # “YYYYMMDDTHHMMSS” This is the end time of the meeting
            timezone:     str,
        }]

    (If no attachments or no ICS blocks are found, “attachments” or “meeting_details” will simply be empty lists.)
    """
    return get_important_emails(limit, days, start_date, end_date, labels)

@app.tool()
def create_task(
    content: str,
    project_name: str,
    description: Optional[str] = None,
    due_string: Optional[str] = None,
    priority: Optional[int] = None,
    labels: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a new task in Todoist under a predefined project.

    Description:
      Adds a task with the given title and optional details to your Todoist account.
      The task will be placed into one of the three predefined projects.

    Args:
      content (str):
        A short title or summary of the task (e.g. "Buy groceries").
      project_name (str):
        Name of the project to add the task into. **Must be one of**:
          - "Meetings"
          - "Shopping"
          - "Reminders"
      description (Optional[str]):
        (Optional) A longer description or notes for the task.
      due_string (Optional[str]):
        (Optional) A human-readable due date (e.g. "today 5pm", "next Monday").
      priority (Optional[int]):
        (Optional) Integer 1–4 where 4 is highest urgency.
      labels (Optional[List[str]]):
        (Optional) List of label names to attach to the task.

    Returns:
      Dict[str, Any]:
        The newly created task object returned by the Todoist API, including fields such as:
          - "id" (int): Unique task identifier.
          - "content" (str): The title you provided.
          - "project_id" (str): The internal project ID.
          - ...and other metadata (due, priority, etc.).
    """
    return add_task(content, project_name, description, due_string, priority, labels)


@app.tool()
def get_tasks(
    project_name: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List active Todoist tasks, optionally filtered by project.

    Description:
      Retrieves all active tasks from your Todoist account. If you specify
      a project name, only tasks in that project are returned.

    Args:
      project_name (Optional[str]):
        (Optional) Name of one of the predefined projects to filter by:
          - "Meetings"
          - "Shopping"
          - "Reminders"
        If omitted or None, returns tasks from all three projects.

    Returns:
      List[Dict[str, Any]]:
        A list of task dictionaries, each containing:
          - "id" (int): Unique task ID.
          - "content" (str): Task title.
          - "project" (str): Project name (one of the three).
          - "description" (str): Task notes (may be empty).
          - "due" (str): Human-readable due date string (may be empty).
          - "priority" (int): 1–4 priority level.
          - "labels" (List[str]): Any attached labels.
    """
    return list_tasks(project_name)


@app.tool()
def update_existing_task(
    task_id: Optional[int] = None,
    query: Optional[str] = None,
    new_content: Optional[str] = None,
    description: Optional[str] = None,
    due_string: Optional[str] = None,
    priority: Optional[int] = None,
    labels: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Update a Todoist task’s fields, by ID or by searching its content.

    Description:
      Modifies one or more properties of an existing task. You must identify
      the task either by its numeric ID or by providing a substring query
      that matches the task’s content; the first match is used.

    Args:
      task_id (Optional[int]):
        (Optional) The Todoist task’s numeric ID. If provided, `query` is ignored.
      query (Optional[str]):
        (Optional) Substring to search within task content if you don’t know the ID.
      new_content (Optional[str]):
        (Optional) New title for the task.
      description (Optional[str]):
        (Optional) New notes or description.
      due_string (Optional[str]):
        (Optional) New human-readable due date string.
      priority (Optional[int]):
        (Optional) New priority level (1–4).
      labels (Optional[List[str]]):
        (Optional) Replacement list of label names (empty list clears labels).

    Returns:
      Dict[str, Any]:
        On success, returns:
          {"status": "success", "task_id": <int>}

    Raises:
      ValueError:
        If neither `task_id` nor a matching `query` is found, or if no fields
        are provided to update.
    """
    return update_task(task_id, query, new_content, description, due_string, priority, labels)


@app.tool()
def delete_existing_task(
    task_id: Optional[int] = None,
    query: Optional[str] = None
) -> bool:
    """
    Delete a Todoist task, by ID or by searching its content.

    Description:
      Removes a task from your Todoist account. Identify the task
      either by its numeric ID or by providing a substring query that
      matches the task content; the first match is deleted.

    Args:
      task_id (Optional[int]):
        (Optional) The numeric Todoist task ID.
      query (Optional[str]):
        (Optional) Substring to search within task content if you don’t know the ID.

    Returns:
      bool:
        True if deletion succeeded, False otherwise.

    Raises:
      ValueError:
        If neither `task_id` nor a matching `query` is found.
    """
    return delete_task(task_id, query)

@app.tool()
def get_weather(location: str) -> List[Dict[str, str]]:
    """
    Description:
      Fetches the daily weather forecast for the next 5 days at the specified location.

    Input:
      - location (str): 
          The name of the city or place to retrieve weather for (e.g., "Lonavala").

    Output:
      Returns a list of 5 dictionaries, one per day. Each dictionary includes:
        - date (str):        Forecast date in "YYYY-MM-DD" format.
        - feels_like (float): "Feels like" temperature in °C.
        - temp_min (float):   Minimum daily temperature in °C.
        - temp_max (float):   Maximum daily temperature in °C.
        - wind_speed (float): Wind speed in m/s.
        - humidity (int):     Relative humidity percentage.
        - rain_mm (float):    Rain volume in mm (0.0 if none).
        - snow_mm (float):    Snow volume in mm (0.0 if none).
        - clouds_pct (int):   Cloud cover percentage.
        - sunrise (str):      Local sunrise time "HH:MM".
        - sunset (str):       Local sunset time "HH:MM".
        - description (str):  Short text weather description (e.g., "light rain").
    """
    return get_5day_forecast(location)

@app.tool()
def get_places(location: str) -> List[Dict[str, str]]:
    """
    Description:
      Retrieves up to N top tourist attractions for the given location, 
      including a brief description and estimated time/distance to visit.

    Input:
      - location (str):
          The name of the city or place to search attractions for (e.g., "Kakinada").

    Output:
      Returns a list of up to `limit` dictionaries, each containing:
        - name (str):          The attraction's name.
        - description (str):   A short summary of the place.
        - time_required (str): Estimated visit duration or distance from center
                               (e.g., "2 to 3 hours", "1 km from city center").
    """
    return get_nearby_places(location)

@app.tool()
def send_whatsapp(name: str, message: str) -> str:
    """
    Looks up contact, builds the WhatsApp click-to-chat URL,
    opens it automatically in the default browser, and returns the URL.
    """
    return open_whatsapp(name, message)

@app.tool()
def create_itinerary(location: str, days: int = 5, place_limit: int = 5) -> List[Dict[str, Any]]:
    """
    Description:
      Creates a day-by-day itinerary for the next `days` days at the specified location,
      combining weather forecasts and top tourist attractions.

    Input:
      - location (str): The place to plan the itinerary for.
      - days (int): Number of days to include in the itinerary (default: 5).
      - place_limit (int): Maximum number of attractions per day (default: 5).

    Output:
      Returns a list of `days` dictionaries, each containing:
        - date (str):    Forecast date in "YYYY-MM-DD" format.
        - weather (dict): Weather details for that date.
        - places (list): List of up to `place_limit` attractions.
    """
    forecasts = get_weather(location)
    attractions = get_places(location)[:place_limit]
    itinerary = []
    for forecast in forecasts[:days]:
        itinerary.append({
            "date": forecast["date"],
            "weather": forecast,
            "places": attractions
        })
    return itinerary

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
