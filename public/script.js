document.addEventListener('DOMContentLoaded', () => {
    const commentsList = document.getElementById('comments-list');
    const commentForm = document.getElementById('comment-form');
    const commentInput = document.getElementById('comment-input');

    function loadComments() {
        fetch('/api/comments')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(comments => {
                console.log("Received comments:", comments);  // Debug log
                commentsList.innerHTML = comments.map(comment => `
                    <div class="comment">
                        <p>${comment.text}</p>
                        <button onclick="deleteComment(${comment.id})">Supprimer</button>
                    </div>
                `).join('');
            })
            .catch(error => console.error('Error loading comments:', error));
    }

    function addComment(event) {
        event.preventDefault();
        const commentText = commentInput.value.trim();
        if (commentText) {
            fetch('/api/comments', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: commentText })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(newComment => {
                console.log("Added new comment:", newComment);  // Debug log
                commentInput.value = '';
                loadComments();  // Refresh the comments list
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Une erreur s\'est produite. Veuillez réessayer.');
            });
        }
    }

    window.deleteComment = function(commentId) {
        if (confirm('Êtes-vous sûr de vouloir supprimer ce commentaire ?')) {
            fetch(`/api/comments/${commentId}`, { method: 'DELETE' })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    loadComments();  // Refresh the comments list
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Une erreur s\'est produite. Veuillez réessayer.');
                });
        }
    };

    commentForm.addEventListener('submit', addComment);
    loadComments();  // Load comments when the page loads
});
