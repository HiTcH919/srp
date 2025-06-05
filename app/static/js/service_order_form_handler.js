// app/static/js/service_order_form_handler.js
document.addEventListener('DOMContentLoaded', function() {
    const storageKey = 'serviceOrderFormData';

    // Function to save data from current step to localStorage
    // Assumes form elements for a step are wrapped in a container with id like 'basic_info_form_fields'
    function saveStepData(stepContainerId) {
        let currentStepData = {};
        const formContainer = document.getElementById(stepContainerId);
        if (!formContainer) {
            console.warn('Form container for step not found:', stepContainerId);
            return;
        }

        // Query all relevant form elements within the specific container
        const formElements = formContainer.querySelectorAll('input, select, textarea');

        formElements.forEach(element => {
            if (element.name) {
                if (element.type === 'checkbox') {
                    // For multiple checkboxes with the same name, store as an array of values
                    if (element.checked) {
                        if (currentStepData[element.name]) {
                            if (!Array.isArray(currentStepData[element.name])) {
                                currentStepData[element.name] = [currentStepData[element.name]];
                            }
                            currentStepData[element.name].push(element.value || element.id); // Use value or id
                        } else {
                            currentStepData[element.name] = element.value || element.id; // If only one, store directly or as array
                        }
                    } else if (!currentStepData[element.name] && formContainer.querySelectorAll(`input[name="${element.name}"][type="checkbox"]`).length > 1) {
                        // Ensure array exists if multiple checkboxes, even if none are checked initially for this element
                        // currentStepData[element.name] = []; // Or handle default empty array elsewhere
                    } else if (formContainer.querySelectorAll(`input[name="${element.name}"][type="checkbox"]`).length === 1 && !element.checked) {
                         currentStepData[element.name] = false; // For single checkbox, false if unchecked
                    }
                } else if (element.type === 'radio') {
                    if (element.checked) {
                        currentStepData[element.name] = element.value;
                    }
                } else if (element.type === 'file') {
                    // For file inputs, store filename(s). Actual file upload is separate.
                    if (element.files && element.files.length > 0) {
                        if (element.files.length === 1) {
                            currentStepData[element.name] = element.files[0].name;
                        } else {
                            currentStepData[element.name] = Array.from(element.files).map(file => file.name);
                        }
                    } else {
                        currentStepData[element.name] = null; // Or empty string
                    }
                } else {
                    // Handle multiple elements with the same name (e.g., for lists of items like officer names)
                    // This logic assumes names like 'officer_name[]' or relies on JavaScript to build arrays for complex lists.
                    // For simplicity, if a name ends with '[]', treat as array.
                    if (element.name.endsWith('[]')) {
                        const actualName = element.name.slice(0, -2);
                        if (!currentStepData[actualName]) {
                            currentStepData[actualName] = [];
                        }
                        if (element.value.trim() !== '') { // Only push non-empty values for array fields
                           currentStepData[actualName].push(element.value);
                        }
                    } else {
                         // If it's a unique field or should overwrite (e.g. a single text input)
                        currentStepData[element.name] = element.value;
                    }
                }
            }
        });

        let allFormData = JSON.parse(localStorage.getItem(storageKey)) || {};
        // Use stepContainerId as the key for this step's data, removing '_form_fields'
        const stepKey = stepContainerId.replace('_form_fields', '');
        allFormData[stepKey] = currentStepData;
        localStorage.setItem(storageKey, JSON.stringify(allFormData));
        console.log('Saved data for step:', stepKey, currentStepData);
        console.log('All form data in localStorage:', allFormData);
    }

    // Function to load all data and populate hidden fields on review page
    function populateReviewForm() {
        const allFormData = JSON.parse(localStorage.getItem(storageKey));
        if (allFormData) {
            const reviewForm = document.getElementById('serviceOrderReviewForm'); // ID of the form on the review page
            if (reviewForm) {
                // Clear existing hidden fields to prevent duplicates
                const existingHiddens = reviewForm.querySelectorAll('input[type="hidden"].generated-field');
                existingHiddens.forEach(hidden => hidden.remove());

                for (const step in allFormData) {
                    for (const key in allFormData[step]) {
                        const value = allFormData[step][key];
                        const inputName = `${step}_${key}`; // e.g., basic_info_service_name

                        if (Array.isArray(value)) {
                            value.forEach((item, index) => {
                                const hiddenInput = document.createElement('input');
                                hiddenInput.type = 'hidden';
                                // For arrays, backend needs to handle multiple values for the same name
                                // or use indexed names like inputName[index] if preferred by backend framework
                                hiddenInput.name = `${inputName}`; // Backend list processing
                                hiddenInput.value = item;
                                hiddenInput.className = 'generated-field';
                                reviewForm.appendChild(hiddenInput);
                            });
                        } else if (typeof value === 'object' && value !== null) {
                            // For simple objects (not arrays), stringify them or flatten
                            const hiddenInput = document.createElement('input');
                            hiddenInput.type = 'hidden';
                            hiddenInput.name = inputName;
                            hiddenInput.value = JSON.stringify(value); // Or handle flattening
                            hiddenInput.className = 'generated-field';
                            reviewForm.appendChild(hiddenInput);
                        } else if (value !== null && value !== undefined) { // Handle null/undefined values appropriately
                            const hiddenInput = document.createElement('input');
                            hiddenInput.type = 'hidden';
                            hiddenInput.name = inputName;
                            hiddenInput.value = value;
                            hiddenInput.className = 'generated-field';
                            reviewForm.appendChild(hiddenInput);
                        }
                    }
                }
                console.log('Populated review form with hidden fields from localStorage.');
            }
        }
    }

    window.clearServiceOrderFormStorage = function() {
        localStorage.removeItem(storageKey);
        console.log('Service order form data cleared from localStorage.');
    }

    // --- Event listeners for "Next" buttons ---
    // Each "Next" button should have an ID and a data-next-url attribute.
    // The form fields for that step should be wrapped in a container with ID '{stepName}_form_fields'.
    const nextButtons = document.querySelectorAll('.next-step-btn');
    nextButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const stepContainerId = this.getAttribute('data-step-id'); // e.g., 'basic_info_form_fields'
            if (stepContainerId) {
                saveStepData(stepContainerId);
            } else {
                console.warn('Next button does not have data-step-id:', this.id);
            }
            const nextUrl = this.getAttribute('data-next-url');
            if (nextUrl) {
                window.location.href = nextUrl;
            } else {
                 console.warn('Next button does not have data-next-url:', this.id);
            }
        });
    });

    // --- On the final review page (new_service_review.html) ---
    if (window.location.pathname.includes('/service/new/review-docs')) {
        populateReviewForm();

        const finalSubmitButton = document.querySelector('.finish-save-btn[type="submit"]');
        if (finalSubmitButton && finalSubmitButton.form) {
            finalSubmitButton.form.addEventListener('submit', function() {
                console.log('Submitting all collected data...');
                // IMPORTANT: Clearing storage here is PREMATURE.
                // It should be cleared only after a SUCCESSFUL server response.
                // For this example, we'll log it. In a real app, you'd handle this in an AJAX success callback
                // or on the success page after redirection.
                // clearServiceOrderFormStorage();
                console.log("localStorage will be cleared upon successful submission via server-side logic or success page JS.");
            });
        }
    }

    // Clear storage when "Start New Service" on dashboard is clicked
    const newServiceBtnDashboard = document.getElementById('newServiceBtnDashboard');
    if (newServiceBtnDashboard) {
        newServiceBtnDashboard.addEventListener('click', function(e) {
            // Check if the link is to the first step of the form
            if (this.href && this.href.includes('/service/new/basic-info')) {
                clearServiceOrderFormStorage();
            }
        });
    }

});
