$(document).ready(function () {
    let flightInfo = {};
    let currentQuestion = 0;

    const questions = [
      "D'accord, pour accéder à votre requête, j'aurai besoin de plusieurs informations.",
      "Pouvez-vous me donner la compagnie aérienne ?",
      "Quelle est la date de départ (YYYY-MM-DD) ?",
      "Quelle est l'heure de départ (HH:MM) ?",
      "Quel est le nom de l'aéroport ou la ville d'origine ?",
      "Quel est le nom de l'aéroport ou la ville de destination ?",
  ];

    const fields = [
      "prompt",
      "compagnie",
      "date_depart",
      "heure_depart",
      "origine",
      "destination",
  ];

    function appendMessage(sender, message) {
        const icon =
            sender === "Bot"
                ? '<i class="fas fa-robot"></i>'
                : '<i class="fas fa-user"></i>';
        const messageClass = sender === "Bot" ? "bot-message" : "user-message";
        const messageContent =
            sender === "Bot"
                ? `<p><strong>${icon} ${sender}:</strong> ${message}</p>`
                : `<p>${message} :${icon}</p>`;

        $("#chat-window").append(
            `<div class="${messageClass}">${messageContent}</div>`
        );
        $("#chat-window").scrollTop($("#chat-window")[0].scrollHeight);
    }

    function askQuestion() {
        if (currentQuestion < questions.length) {
        appendMessage("Bot", questions[currentQuestion]);
        if (currentQuestion > 0) {
              $("#chat-form").data("field", fields[currentQuestion]);
          }
      } else {
          saveFlightInfo();
      }
  }

    function validateAnswerWithAI(question, answer, callback) {
        $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/validate_answer",
        data: JSON.stringify({ question: question, answer: answer }),
        success: function (response) {
            callback(response.valid, response.error, response.payload);
        },
        error: function (xhr, status, error) {
            console.error("Erreur lors de la requête:", error);
            callback(false, "Erreur lors de la requête.");
        },
    });
  }

    function saveFlightInfo() {
        $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/save_flight_info",
        data: JSON.stringify(flightInfo),
        success: function (response) {
            appendMessage("Bot", response.message);
        },
        error: function (xhr, status, error) {
            console.error("Erreur lors de la requête:", error);
        },
    });
  }

    $("#chat-form").on("submit", function (e) {
        e.preventDefault();
      let userAnswer = $("#user-input").val().trim();
      let field = $("#chat-form").data("field");

      if (userAnswer === "") return; // Do nothing if the input is empty

      appendMessage("Utilisateur", userAnswer);
      $("#user-input").val("");

      if (currentQuestion > 0) {
        validateAnswerWithAI(
            questions[currentQuestion],
            userAnswer,
            function (isValid, error, payload) {
                if (!isValid) {
              appendMessage(
                  "Bot",
                  error || "Réponse invalide. Veuillez réessayer."
              );
              return;
          }
            if (
                field === "compagnie" ||
                field === "origine" ||
                field === "destination"
            )
                flightInfo[field] = payload;
          else flightInfo[field] = userAnswer;

            currentQuestion++;
            askQuestion();
          }
      );
    } else {
        if (userAnswer === "") return; // Do nothing if the input is empty

        flightInfo["prompt"] = userAnswer;
        currentQuestion++;
        askQuestion();
    }

      $("#chat-window").scrollTop($("#chat-window")[0].scrollHeight);
  });
    // Initialiser la conversation
    appendMessage("Bot", "Comment puis-je vous aider aujourd'hui ?");
    $("#chat-form").data("field", "prompt");

    //   // Ajouter un écouteur d'événement pour la première entrée utilisateur
    //   $("#chat-form").one("submit", function (e) {
    //     e.preventDefault();
    //     askQuestion();
    //   });
    debugger;
    // Ajouter un écouteur d'événement pour la première entrée utilisateur
    $("#chat-form").one("submit", function (e) {
        e.preventDefault();
      let userRequest = $("#user-input").val().trim();
      if (userRequest === "") {
          return; // Do nothing if the input is empty
      }
      appendMessage("Utilisateur", userRequest);
      $("#user-input").val("");
      askQuestion();
  });
});
