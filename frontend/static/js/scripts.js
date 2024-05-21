$(document).ready(function() {
    $('#chat-form').on('submit', function(e) {
        e.preventDefault();

        const userInput = $('#user-input').val();
        if (userInput.trim() === '') {
            return;
        }

        // Afficher le message de l'utilisateur dans la fenêtre de chat
        $('#chat-window').append(`<div class="text-white"><strong>Vous:</strong> ${userInput}</div>`);

        // Envoyer le message à l'API Flask
        $.post('/chat', { message: userInput }, function(data) {
            // Afficher la réponse du bot dans la fenêtre de chat
            $('#chat-window').append(`<div><strong>Bot:</strong> ${data.response}</div>`);
            // Ajouter le message dans la liste des prompts
            $('#chat-prompts').append(`<li class="nav-item">${data.response}</li>`);
            // Vider le champ de saisie
            $('#user-input').val('');
            // Faire défiler vers le bas
            $('#chat-window').scrollTop($('#chat-window')[0].scrollHeight);
        });
    });
});
