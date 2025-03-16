console.log('send_notification.js loaded'); // Ensure file loading

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded'); 

    const courseSection = document.getElementById('courseSelection');
    const recipientSection = document.getElementById('recipientSelection');
    const targetRadios = document.querySelectorAll('input[name="target_type"]');

    console.log('Number of radio buttons:', targetRadios.length); // Make sure to find the element

    function toggleSections() {
        console.log('toggleSections called'); // Make sure the function is called
        const selectedValue = document.querySelector('input[name="target_type"]:checked').value;
        console.log('Selected Value:', selectedValue); 
        console.log('Recipient Section Display:', recipientSection.style.display);
        courseSection.style.display = selectedValue === 'course' ? 'block' : 'none';
        recipientSection.style.display = selectedValue === 'specific' ? 'block' : 'none';
    }

    // Check at initialization
    toggleSections();

    // Bind event listening
    targetRadios.forEach(radio => {
        radio.addEventListener('change', toggleSections);
    });
});