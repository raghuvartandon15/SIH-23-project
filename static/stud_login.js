        function validateForm() {
            var email = document.getElementById('email').value;
            var password = document.getElementById('password').value;

            if (email.trim() === '' || password.trim() === '') {
                alert('Please enter both email and password.');
                return false;
            }

            // You can add more sophisticated validation logic if needed.

            return true;
        }