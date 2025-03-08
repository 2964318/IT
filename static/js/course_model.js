document.addEventListener('DOMContentLoaded', function() {
    $('#editCourseModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        const form = $(this).find('form');
        form.attr('action', form.attr('action').replace('0', button.data('course-id')));
        form.find('[name="code"]').val(button.data('course-code'));
        form.find('[name="name"]').val(button.data('course-name'));
        form.find('[name="credits"]').val(button.data('course-credits'));
        form.find('[name="capacity"]').val(button.data('course-capacity'));
    });
});
