$(document).ready(function() {
    let flightInfo = {};
    let currentQuestion = 0;

    const questions = [
        'D\'accord, pour accéder à votre requête, j\'aurai besoin de plusieurs informations.',
        'Pouvez-vous me donner la compagnie aérienne ?',
        'Quelle est la date de départ (YYYY-MM-DD) ?',
        'Quelle est l\'heure de départ (HH:MM) ?',
        'Quel est le nom de l\'aéroport ou la ville d\'origine ?',
        'Quel est le nom de l\'aéroport ou la ville de destination ?'
    ];

    const fields = [
        'null',
        'compagnie',
        'date_depart',
        'heure_depart',
        'origine',
        'destination'
    ];

    function askQuestion() {
        if (currentQuestion < questions.length) {
            $('#chat-window').append('<p><strong>Bot:</strong> ' + questions[currentQuestion] + '</p>');
            if (currentQuestion > 0) {
                $('#chat-form').data('field', fields[currentQuestion]);
            }
        } else {
            saveFlightInfo();
        }
    }

    function validateAnswerWithAI(question, answer, callback) {
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/validate_answer',
            data: JSON.stringify({ question: question, answer: answer }),
            success: function(response) {
                callback(response.valid, response.error, response.payload);
            },
            error: function(xhr, status, error) {
                console.error('Erreur lors de la requête:', error);
                callback(false, 'Erreur lors de la requête.');
            }
        });
    }

    function saveFlightInfo() {
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/save_flight_info',
            data: JSON.stringify(flightInfo),
            success: function(response) {
                $('#chat-window').append('<p><strong>Bot:</strong> ' + response.message + '</p>');
            },
            error: function(xhr, status, error) {
                console.error('Erreur lors de la requête:', error);
            }
        });
    }

    $('#chat-form').on('submit', function(e) {
        e.preventDefault();
        let userAnswer = $('#user-input').val().trim();
        let field = $('#chat-form').data('field');

        if (currentQuestion > 0) {
            validateAnswerWithAI(questions[currentQuestion], userAnswer, function (isValid, error, payload) {
                if (!isValid) {
                    $('#chat-window').append('<p><strong>Bot:</strong> ' + (error || 'Réponse invalide. Veuillez réessayer.') + '</p>');
                    $('#user-input').val('');
                    return;
                }
                if (field === 'compagnie' || field === 'origine' || field === 'destination')
                    flightInfo[field] = payload;
                else
                    flightInfo[field] = userAnswer
                $('#chat-window').append('<p><strong>Utilisateur:</strong> ' + userAnswer + '</p>');
                $('#user-input').val('');

                currentQuestion++;
                askQuestion();
            });
        } else {
            $('#chat-window').append('<p><strong>Utilisateur:</strong> ' + userAnswer + '</p>');
            flightInfo['prompt'] = userAnswer;
            $('#chat-window').append('<p><strong>Bot:</strong> ' + "Je vais vous poser une series de questions" + '</p>');
            $('#user-input').val('');
            currentQuestion++;
            askQuestion();
        }

        $('#chat-window').scrollTop($('#chat-window')[0].scrollHeight);
    });
    // Initialiser la conversation
    $('#chat-window').append('<p><strong>Bot:</strong> Comment puis-je vous aider aujourd\'hui ?</p>');

    $('#chat-form').data('field', 'null');


    // Ajouter un écouteur d'événement pour la première entrée utilisateur
    $('#chat-form').one('submit', function(e) {
        e.preventDefault();
        askQuestion();
    });
});
