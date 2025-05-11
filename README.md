
Built by https://www.blackbox.ai

---

# Inventory & POS System

## Project Overview
The Inventory & POS System is a comprehensive web application designed to manage inventory, financial transactions, and stock transfers seamlessly. The application provides functionality for logging in, managing products, processing sales through a Point of Sale (POS) module, and generating reports.

## Installation
To set up the Inventory & POS System locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/inventory-pos-system.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd inventory-pos-system
   ```

3. **Open the `index.html` file in your web browser:**
   - You can simply double-click the `index.html` file or use a local server if necessary.

## Usage
1. **Login:**
   - Open the application in your browser and log in using any credentials (the login is a demo functionality for displaying the dashboard).

2. **Explore the Dashboard:**
   - After logging in, you will be directed to the dashboard where you can view quick stats, recent activities, and access various sections.

3. **Manage Inventory:**
   - Access the ‘Inventory Management’ section from the sidebar to view or manage the products.

4. **Process Sales:**
   - Navigate to the POS section to search for products, add them to the cart, and proceed with payments.

5. **Transfer Stock:**
   - Use the 'Stock Transfer' section for managing stock movements between branches.

6. **Generate Reports:**
   - Check the reports section for analytics and summaries of sales and inventory.

## Features
- **User Authentication:** Simple login system with demo access.
- **Product Management:** Add, edit, remove, and view products in the inventory.
- **Point of Sale (POS):** Process sales with cash and QRIS payment options.
- **Stock Transfers:** Manage stock transfers between branches.
- **Analytics and Reporting:** View detailed reports of sales and inventory status.

## Dependencies
The project uses the following dependencies, primarily through external CDNs:
- **Tailwind CSS**: A utility-first CSS framework.
- **Font Awesome**: For icons.
- **Google Fonts**: Custom font styles.

```html
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## Project Structure
The project consists of several key HTML files, each corresponding to different functionalities:

```
├── index.html           # Main login page and dashboard
├── pos.html             # Point of Sale page
├── inventory.html       # Inventory management page
├── transfer.html        # Stock transfer management page
└── reports.html         # Reports and analytics page
```

Each HTML file contains:
- **Tailwind CSS** for styling.
- Icons and fonts from Font Awesome and Google Fonts.
- JavaScript for handling dynamic interactions and functionalities.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or fixes.

## License
This project is open-source and available under the MIT License.