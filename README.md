# TP24 Group API Test

## Summary

- Time recorded: **~3 hours**
- Language used: **Python**
- Framework used: **FastAPI**
- Database used: **SQLite**

## How to run

- Create a `.env` file in the root directory with the content as similar to `.env.example` file
- Filled in the `.env` file with the values of your choice. The database of my choice in this example is SQLite, but you
  can use any relational database of your choice.
- Make sure your machine has Python 3.8 installed, and then create a virtual env using the following command:
  ```
    python3.8 -m venv venv
    source venv/bin/activate # Unix
    venv\Scripts\activate.bat # Windows
  ```
- Install the dependencies using the following command:
  ```
    pip install -r requirements.txt
  ```
- Run the application using the following command:
  ```
    uvicorn app.api.main:app --reload
  ```
- The application Swagger API docs will be available at `http://localhost:8000/docs`
- Proceed with sending requests to the API endpoints

## API Endpoints

**Note**: The API endpoints are protected with API key in the headers. You can set the API key in the `.env` file.

1. **Create receivables**:

    * Request:
        ```
        POST /api/receivables
        ```
        ```
        [
          {
            "reference": "string",
            "currencyCode": "string",
            "issueDate": "2023-10-14",
            "openingValue": 0,
            "paidValue": 0,
            "dueDate": "2023-10-14",
            "closedDate": "2023-10-14",
            "cancelled": true,
            "debtorName": "string",
            "debtorReference": "string",
            "debtorAddress1": "string",
            "debtorAddress2": "string",
            "debtorTown": "string",
            "debtorState": "string",
            "debtorZip": "string",
            "debtorCountryCode": "string",
            "debtorRegistrationNumber": "string"
          },
          {...}
       ]
        ```

2. **Get receivables summary**:

* `GET /api/receivables/summary?debtorName=<name_of_debtor>&untilDate=<date_until_due_date>`

## Testing

* To run the test, run the following command:
    ```
    pytest tests/
    ```

## Engineering Decision & Assumptions

* I chose **FastAPI** to develop because this is a modern, relatively easy framework to use to develop RESTFUL API
* I chose **SQLite** as the database because it is a lightweight database that is easy to set up and use. It is also
  relational, which is suitable for this use case.
* I chose **Python** because I'm quite familiar with it, and it's quicker to accomplish the task with it.
* I added two query parameters in the *get receivables summary* endpoints because I assume that the API should be able
  to filter the receivables by some attributes, and I thought those 2 attributes are the most obvious ones to be. This
  is also the reason why I indexed those 2 attributes in the database for fast retrieval