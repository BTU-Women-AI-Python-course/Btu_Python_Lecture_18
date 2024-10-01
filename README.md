# Django REST Framework 

- **Pagination** - https://www.django-rest-framework.org/api-guide/pagination/:
  - Efficiently handle large datasets by delivering data in manageable chunks, enhancing performance and user experience.
- **Django Filters** - https://www.django-rest-framework.org/api-guide/filtering/:
  - Add filtering capabilities to your API endpoints, allowing clients to retrieve only the necessary data and making your API more flexible.
- **Custom Permissions** - https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions:
  - Define and apply custom permissions to control access to specific parts of your API, ensuring security and privacy.
- **ViewSet Extra Actions** - https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
- **Authentication** - https://www.django-rest-framework.org/api-guide/authentication/


## 📚 Task: Implement Pagination, Filtering, and Custom Permissions

### 1. Add Pagination to the `Book` API:
- Implement pagination in the `BookViewSet` using DRF’s built-in pagination classes.
- Set up `PageNumberPagination` to limit the results to 10 books per page.

### 2. Add Django Filtering to the `Book` API:
- Install `django-filter` and configure it to allow filtering books by `author` and `published_date`.
- Ensure the client can pass query parameters like `author` or `published_date` to filter the book list.

### 3. Implement Custom Permissions:
- Create a custom permission class to allow only the author of a book (or an admin) to update or delete a book.
- Apply the custom permission to the `BookViewSet` to restrict updates and deletions.
