import java.sql.Date;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import dev.failsafe.internal.util.Assert;

public class register {
    public static void main(String[] args) throws Exception {
        System.out.println("Hello, World!");
        System.setProperty("webdriver.chrom.driver",
                "C:\\Users\\parik\\Downloads\\chrome-win32.zip\\chrome-win32\\chromedriver.exe");
        WebDriver driver = new ChromeDriver();

        // Navigate to the website
        driver.get("http://127.0.0.1:5000");

        // Find and click the register button
        WebElement registerButton = driver.findElement(By.id("register_nav_button"));
        registerButton.click();

        // Fill in the registration form
        WebElement firstNameField = driver.findElement(By.id("firstName"));
        WebElement lastNameField = driver.findElement(By.id("lastName"));
        WebElement emailField = driver.findElement(By.id("email"));
        WebElement phoneNumberField = driver.findElement(By.id("phoneNumber"));
        WebElement passwordField = driver.findElement(By.id("password"));
        WebElement confirmPasswordField = driver.findElement(By.id("confirm_password"));

        // Fill in the form fields
        firstNameField.sendKeys("YourFirstName");
        lastNameField.sendKeys("YourLastName");
        emailField.sendKeys("esata@example.com");
        phoneNumberField.sendKeys("1234567890");
        passwordField.sendKeys("your_password");
        confirmPasswordField.sendKeys("your_password");

        // Submit the registration form
        WebElement registerForm = driver.findElement(By.id("register_form_id"));
        registerForm.submit();

        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("Successful");

        // Find and click the login button
        WebElement loginButton = driver.findElement(By.id("login_nav_button"));
        loginButton.click();

        // Fill in the login form
        WebElement emailFieldLogin = driver.findElement(By.name("email"));
        WebElement passwordFieldLogin = driver.findElement(By.name("password"));
        // login form
        emailFieldLogin.sendKeys("qwer@gmail.com");
        passwordFieldLogin.sendKeys("qwe");

        // Submit the login form
        WebElement loginForm = driver.findElement(By.className("btn"));
        // form
        loginForm.submit();

        // Wait for a while to let the page load
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Click the detail button for the first hotel
        WebElement detailButton = driver.findElement(By.id("Detail_button"));
        detailButton.click();

        // // Get the current date and the checkout date (3 days from now)
        // LocalDate currentDate = LocalDate.now();
        // LocalDate checkoutDate = currentDate.plusDays(3);

        // // Format dates in the required format
        // DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy hh:mm
        // a");
        // String formattedCheckInDate = currentDate.format(formatter);
        // String formattedCheckOutDate = checkoutDate.format(formatter);

        // // Set the check-in date
        // WebElement checkInDateInput = driver.findElement(By.id("check_in_date"));
        // checkInDateInput.sendKeys(formattedCheckInDate);

        // // Set the check-out date
        // WebElement checkOutDateInput = driver.findElement(By.id("check_out_date"));
        // checkOutDateInput.sendKeys(formattedCheckOutDate);

        // // Enter guest capacity
        // WebElement guestCapacity = driver.findElement(By.id("guests")); // Replace
        // with the actual ID of your
        // // guest capacity input
        // guestCapacity.sendKeys("2"); // Replace with the desired guest capacity

        // // Click the check availability button
        // WebElement checkAvailabilityButton =
        // driver.findElement(By.id("check_availability_button_id")); // Replace with
        // // the actual ID
        // // of your check
        // // availability
        // // button
        // checkAvailabilityButton.click();

        // // Wait for a while to let the page load
        // try {
        // Thread.sleep(1000);
        // } catch (InterruptedException e) {
        // e.printStackTrace();
        // }

        // // Enter payment details
        // WebElement cardNumber = driver.findElement(By.id("cardNumber")); // Replace
        // with the actual ID of your card
        // // number input
        // WebElement cardName = driver.findElement(By.id("nameOnCard")); // Replace
        // with the actual ID of your card name
        // // input
        // WebElement ccv = driver.findElement(By.id("cvv")); // Replace with the actual
        // ID of your ccv input
        // WebElement expiryDate = driver.findElement(By.id("expireDate")); // Replace
        // with the actual ID of your
        // // expiry date input

        // cardNumber.sendKeys("1234567890123456"); // Replace with the actual card
        // number
        // cardName.sendKeys("Card Holder"); // Replace with the actual cardholder name
        // ccv.sendKeys("123"); // Replace with the actual CCV
        // expiryDate.sendKeys("12/25"); // Replace with the actual expiry date

        // // Click the pay and book button
        // WebElement payAndBookButton =
        // driver.findElement(By.id("pay_and_book_button_id")); // Replace with the
        // actual ID
        // // of your pay and book
        // // button
        // payAndBookButton.click();

        // // Wait for a while to let the payment process (you may need to adjust this
        // // timing)
        // try {
        // Thread.sleep(10000);
        // } catch (InterruptedException e) {
        // e.printStackTrace();
        // }

        // Close the browser window
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Click the booking button
        WebElement bookingButton = driver.findElement(By.id("Bookingss"));
        bookingButton.click();

        // Wait for a while to let the page load
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Click the feedback button
        WebElement feedbackButton = driver.findElement(By.id("Feedbacks"));
        feedbackButton.click();

        // Wait for a while to let the page load
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Enter feedback and click post feedback button
        WebElement feedbackInput = driver.findElement(By.id("feedback_area"));
        feedbackInput.sendKeys("This is a sample feedback.");
        WebElement postFeedbackButton = driver.findElement(By.id("post_feedback"));
        postFeedbackButton.click();

        // Wait for a while to let the page load
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Click the enquiries button
        WebElement enquiriesButton = driver.findElement(By.id("Enquiries"));
        enquiriesButton.click();

        // Wait for a while to let the page load
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Enter enquiries and click post enquiry button
        WebElement enquiriesInput = driver.findElement(By.id("enquiries_input_id"));
        enquiriesInput.sendKeys("This is a sample enquiry.");

        WebElement postEnquiryButton = driver.findElement(By.id("post_enquiry_button_id"));
        postEnquiryButton.click();

        // Wait for a while to let the page load
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Click the change password button
        WebElement changePasswordButton = driver.findElement(By.id("change-password"));
        changePasswordButton.click();

        // Wait for a while to let the page load
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Enter old and new password, then click update button
        WebElement oldPasswordInput = driver.findElement(By.id("password"));
        WebElement newPasswordInput = driver.findElement(By.id("confirm_password"));

        oldPasswordInput.sendKeys("qwe");
        newPasswordInput.sendKeys("qwe");

        WebElement updateButton = driver.findElement(By.id("update_button_id"));
        updateButton.click();

        // Wait for a while to let the page load
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Click the home button
        WebElement homeButton = driver.findElement(By.id("home"));
        homeButton.click();

        // Wait for a while to let the page load
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        driver.quit();
    }
}
