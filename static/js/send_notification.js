document.addEventListener('DOMContentLoaded', function() {
    const courseSection = document.getElementById('courseSelection');
    const courseRadios = document.querySelectorAll('input[name="target_type"]');

    function toggleCourseVisibility() {
        const selectedValue = document.querySelector('input[name="target_type"]:checked').value;
        courseSection.style.display = selectedValue === 'course' ? 'block' : 'none';
    }

    toggleCourseVisibility();

    courseRadios.forEach(radio => {
        radio.addEventListener('change', toggleCourseVisibility);
    });
});
