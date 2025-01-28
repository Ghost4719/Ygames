function deleteComment(commentId) {
    if (confirm('Are you sure you want to delete this comment?')) {
        // Send a delete request to the admin
        fetch(`/admin/usat/comment/${commentId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
            },
        })
        .then(response => {
            if (response.ok) {
                alert('Comment deleted successfully!');
                location.reload();  // Reload the page to update the UI
            } else {
                alert('Failed to delete comment');
            }
        })
        .catch(error => {
            console.error('Error deleting comment:', error);
        });
    }
}
