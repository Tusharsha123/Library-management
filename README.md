# Library Management System

A complete Library Management System built with PHP, MySQL, HTML, CSS, JavaScript, and Bootstrap.

## Features

- Admin login with secure password hashing
- Dashboard with totals for books, members, issued books, returned books, and pending returns
- Full book management CRUD
- Full member management CRUD
- Book issue and return process with automatic fine calculation
- Reports with browser PDF export support
- Input validation and prepared statements to prevent SQL injection

## Installation

1. Install XAMPP and start Apache and MySQL.
2. Place this project folder inside `htdocs` (for example `C:\xampp\htdocs\library-management`).
3. Import `database/library_management.sql` into MySQL using phpMyAdmin or the MySQL command line.
4. Update `config/db.php` if your MySQL username, password, or database name are different.
5. Open `http://localhost/library-management/` in your browser.

## Default Admin Credentials

- Username: `admin`
- Password: `admin123`

## Notes

- Use the `Reports` section to view books, members, issued books, and fines.
- Click `Export to PDF` on report pages to generate a printable PDF via browser print.
