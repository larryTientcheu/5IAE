$(document).ready(function() {
    $('#chat-form').on('submit', function(e) {
        e.preventDefault();
        var userQuestion = $('#user-input').val();
        $('#chat-window').append('<p><strong>Utilisateur:</strong> ' + userQuestion + '</p>');
        
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/get_response',
            data: JSON.stringify({ question: userQuestion }),
            success: function(response) {
                $('#chat-window').append('<p><strong>Chatbot:</strong> ' + response.response + '</p>');
                $('#user-input').val('');
                $('#chat-window').scrollTop($('#chat-window')[0].scrollHeight);
            },
            error: function(xhr, status, error) {
                console.error('Erreur lors de la requête:', error);
            }
        });
    });
});
