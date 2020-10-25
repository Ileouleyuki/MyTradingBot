/** 
*        _                                _       _   
*       | |                              (_)     | |  
*       | | __ ___   ____ _ ___  ___ _ __ _ _ __ | |_ 
*   _   | |/ _` \ \ / / _` / __|/ __| '__| | '_ \| __|
*  | |__| | (_| |\ V / (_| \__ \ (__| |  | | |_) | |_ 
*   \____/ \__,_| \_/ \__,_|___/\___|_|  |_| .__/ \__|
*                                          | |        
*                                          |_|                            
* =============================================================================================
* NOM 		>> app.js
* TYPE 	    >> Fichier JavaScript 
* AUTEUR	>> ileouleyuki
* CREATION	    >> 28/12/2019
* DESCRIPTION   >> Fichier JavaScript regroupant toutes les fonctions Communes
* =============================================================================================
*/

/*
 * Variables de configuration
 * Un objet avec une valeur-clé paris assignée dans TWIG
 *
 * @see footer.php
 * @see core/Controller.php
 */
// =============================================================================================
// APP 
// =============================================================================================
// TYPE 	        >> Fonction de base pour l'app
// AUTEUR	        >> Julien DENIS Chef de projet ORANGE - UPR Ouest
// CREATION	        >> 28/12/2019
// DESCRIPTION      >> Aide appel AJAX
// =============================================================================================
var app = {
    /**
    * Affichage de l'horloge
    */
    clock: function () {
        moment.locale('fr');
        document.getElementById("Horloge").innerHTML = '<i class="fas fa-clock"></i>&nbsp&nbsp' + moment().format("ddd Do MMM YYYY") + "&nbsp" + moment().format("H:mm:ss") + ' (S' + moment().format("WW") + ')';
        // Repetition toute les 1000ms
        setTimeout("app.clock()", 1000);
    },
    /**
    * Affichage du Loader
    */
    startLoader: function (selector) {
        $(selector).css('position', 'relative');
        $(selector).append('<div class="loading"></div>');
        $("body").css("padding-top", $(".navbar-fixed-top").height());

    },
    /**
    * Arret du Loader
    */
    stopLoader: function (selector) {
        $(selector).css('position', 'static');
        $('.loading').remove();
    },
    /**
    * Traitement des données JSON pour les affichage de tableau
    */
    loadTable: function (json) {
        app.closeModalLoader()
        if ((json.cat == "SUCCESS") || (json.cat == "INFO")) {
            // notify.info(json)
            return true
        } else {
            notify.error(json)
            app.stopLoader('body')
            return false
        }
    },
    /**
    * Affichage de la Fenetre Modal Loader
    */
    showModalLoader: function (selector) {
        $("#loadMe").modal({
            backdrop: "static", //remove ability to close modal with click
            keyboard: false, //remove option to close with keyboard
            show: true //Display loader!
        });
        $("#progress-title-modal").html('<i class="fas fa-play-circle"></i>&nbspDemarrage');
        $('#progress-txt-modal').empty();
        $( '#btn-close' ).prop("disabled", true);
        $( "#btn-close" ).addClass( "d-none" );
      
    },
    /**
    * Fermeture de la Fenetre Modal Loader
    */
    closeModalLoader: function (selector) {
        $("#loadMe").modal("hide")
    },
    /**
    * Lancement d'un mail (Lien MAILTO)
    */
    createMailto: function (email, sujet, body, attachement) {
        //Create a object of Outlook.Application
        try {
            var mailto_link = 'mailto:' + email + '?subject=' + sujet + '&body=' + body;
            win = window.open(mailto_link, 'emailWindow');
            if (win && win.open && !win.closed) win.close();
        }
        catch (err) {
            alert("Outlook configuration error." + err.message);
        }
    },
    /**
    * Verification des infos triplet
    * 
    */
    verifTriplet: function (checkSchema=true) {
        // -- Verification si selection serveur est null
        if ( $("#serveur").val().trim().length == 0){
            notify.warning({"mess":"Veuillez selectionner un Serveur de Travail", "oper": "Choix Triplet"})
            return false
        }
        // -- Verification si selection serveur est null
        if ( $("#database").val().trim().length == 0){
            notify.warning({"mess":"Veuillez selectionner une base de donnée de Travail", "oper": "Choix Triplet"})
            return false
        }
        if(checkSchema == true){ 
            // -- Verification si selection serveur est null
            if ( $("#schema").val().trim().length == 0){
                notify.warning({"mess":"Veuillez selectionner un Schema de Travail", "oper": "Choix Triplet"})
                return false
            }
        }
        return true

    },

}
// =============================================================================================
// MODAL
// =============================================================================================
// TYPE 	>> Fonctions Affichage Modal Basique
// AUTEUR	>> Julien DENIS Chef de projet ORANGE - UPR Ouest
// CREATION	>> 28/12/2019
// DESCRIPTION  >> Liste de Fonctions permettant l'affichage des Notifications
// =============================================================================================
// -- Definition du locale
bootbox.setLocale("fr");
// -- Creation Objet
var modal = {
    /**
     * Affichage d'une fenetre OUI/NON
     * 
     * @param {*} question 
     * @param {*} MyFunction Fonction à executer si oui 
     */
    promptYesOrNo: function (question, MyFunction) {
        bootbox.confirm({
            title: "<i class='fas fa-question-circle'></i>&nbspQuestion",
            message: question,
            buttons: {
                cancel: {
                    label: '<i class="fa fa-times"></i>&nbspNON',
                    className: "btn btn-danger",
                },
                confirm: {
                    label: '<i class="fa fa-check"></i>&nbspOUI',
                    className: "btn btn-success",
                }
            },
            callback: function (result) {
                if (result === true) {
                    eval(MyFunction);
                }
            }
        });
    }
}

// =============================================================================================
// NOTIFICATION
// =============================================================================================
// NOM 		>> app_notify.js
// TYPE 	>> Fonctions de Notifications
// AUTEUR	>> Julien DENIS -- UPR Ouest -- PCN
// CREATION	>> 29/01/2020
// DESCRIPTION  >> Liste de Fonctions permettant l'affichage des Notifications
// =============================================================================================

var notify = {
    /**
     * Notification de SUCCES
     * 
     * @param {*} MESSAGE 
     */
    success: function (data) {
        if (data.silent == true){
            return
        }
        // -- Affichage de la Notification
        $.notify({
            // options
            message: '<p class="mb-0">' + data.mess + '</p>',
            title: '<strong><i class="fas fa-smile-beam"></i>&nbsp' + data.oper + '</strong>',
            //url: 'https://github.com/mouse0270/bootstrap-notify',
            //target: '_blank'
        }, {
            // settings
            type: 'success',
            newest_on_top: false,
            placement: {
                from: "top",
                align: "center"
            },
            animate: {
                enter: 'animated fadeInDown',
                exit: 'animated fadeOutUp'
            },
            delay: 0,
            //timer: 1000,

        });
    },
    /**
     * Notification de WARNING
     * 
     * @param {*} MESSAGE 
     */
    warning: function (data) {
        // -- Affichage de la Notification
        $.notify({
            // options
            message: '<p class="mb-0">' + data.mess + '</p>',
            title: '<strong><i class="fas fa-exclamation-triangle"></i>&nbsp' + data.oper + '</strong>',
            //url: 'https://github.com/mouse0270/bootstrap-notify',
            //target: '_blank'
        }, {
            // settings
            type: 'warning',
            newest_on_top: false,
            placement: {
                from: "top",
                align: "center"
            },
            animate: {
                enter: 'animated fadeInDown',
                exit: 'animated fadeOutUp'
            },
            delay: 0,
            //timer: 1000,

        });
    },
    /**
     * Notification des ERREURS
     * 
     * @param {*} MESSAGE 
     */
    error: function (data) {
        console.log(data)
        // -- Affichage de la Notification
        $.notify({
            // options
            message: '<p class="mb-0">' + data.mess + '</p>',
            title: '<strong><i class="fas fa-skull-crossbones"></i>&nbsp' + data.oper + '</strong>',
            //url: 'https://github.com/mouse0270/bootstrap-notify',
            //target: '_blank'
        }, {
            // settings
            type: 'danger',
            newest_on_top: false,
            placement: {
                from: "top",
                align: "center"
            },
            animate: {
                enter: 'animated fadeInDown',
                exit: 'animated fadeOutUp'
            },
            delay: 0,
            //timer: 1000,

        });


    },
    /**
     * Notification de INFO
     * 
     * @param {*} MESSAGE 
     */
    info: function (data) {
        // -- Affichage de la Notification
        $.notify({
            // options
            message: '<p class="mb-0">' + data.mess + '</p>',
            title: '<strong><i class="fas fa-info-circle"></i>&nbsp' + data.oper + '</strong>',
            //url: 'https://github.com/mouse0270/bootstrap-notify',
            //target: '_blank'
        }, {
            // settings
            type: 'info',
            newest_on_top: false,
            placement: {
                from: "top",
                align: "center"
            },
            animate: {
                enter: 'animated fadeInDown',
                exit: 'animated fadeOutUp'
            },
            delay: 5000,
            timer: 1000,
            //timer: 1000,

        });
    }
}
// =============================================================================================
// HELPERS 
// =============================================================================================
// TYPE 	        >> Aide pour traitement des données
// AUTEUR	        >> Julien DENIS Chef de projet ORANGE - UPR Ouest
// CREATION	        >> 28/12/2019
// DESCRIPTION      >> Aide pour traitement des données
// =============================================================================================
var helpers = {
    /**
    * Transformation d'un formulaire en FormData
    * 
    * @param {type} form Identifiant formulaire à Serializer
    */
    serializetoFormData: function (reference, toJSON = true) {
        // -- Initialisation du FormData
        var formData = new FormData();
        // -- Verification existence de la reference
        if ($(reference).length == 0) {
            console.log("L'element DOM (Form) " + reference + " n'existe pas")
            return
        }
        // -- Serialisation en Array
        var form_data = $(reference).serializeArray();
        // -- Ajout des Inputs dans le FormData
        $.each(form_data, function (key, input) {
            formData.append(input.name, input.value);
        });
        // -- [SPECIAL] -- InputFile
        if ($(reference).has("file")) {
            $.each($(reference).find("input[type=file]"), function (index, field) {
                $.each($(field)[0].files, function (index, file) {
                    formData.append(field.name, file);
                });
            });
        }
        // -- [SPECIAL] -- TextArea CKEDITOR
        if ($(reference).has("textarea")) {
            $.each($(reference).find('textarea'), function (i, textarea) {
                //console.log(textarea)
                //CKEDITOR.instances()
                if (Object.keys(formData).indexOf(textarea.name) === -1) {
                    if (window.CKEDITOR && CKEDITOR.instances[textarea.name]) {
                        formData.set(textarea.name, CKEDITOR.instances[textarea.name].getData());
                    } else {
                        formData.set(textarea.name, textarea.value);
                    }
                } else {
                    formData.append(textarea.name, textarea.value)
                }
                // Object.keys(formData).indexOf(textarea.name) === -1 ? formData.append(textarea.name, textarea.value) : formData[textarea.name]= textarea.value;
            });
        }
        // -- [SPECIAL] -- Input CheckBox
        if ($(reference).has("checkbox")) {
            $.each($(reference).find('input[type="checkbox"]'), function (i, tag) {
                if (Object.keys(formData).indexOf(tag.name) === -1) {
                    formData.set(tag.name, $('input[name="' + tag.name + '"]').prop('checked'));
                } else {
                    formData.append(tag.name, $('input[name="' + tag.name + '"]').prop('checked'))
                }
            });
        }
        // [DEBUG] -- Affichage des Entrées
        //console.log(Object.fromEntries(formData));
        // -- Renvoi d'un objet JSON si tiJSON est a true
        if(toJSON == true){
            var jsonObject = {};
            for (const [key, value]  of formData.entries()) {
                jsonObject[key] = value;
            }
            return jsonObject; 
        }else{
            // -- Retour du FormData
            return formData;
        }
    },
    /**
     * Ajouter le jeton csrf aux données qui seront envoyées en ajax
     *
     * @param  mixed  data
     *
     */
    appendCsrfToken: function (data) {

        if (typeof (data) === "string") {
            if (data.length > 0) {
                data = data + "&csrfToken=" + config.csrfToken;
            } else {
                data = data + "csrfToken=" + config.csrfToken;
            }
        }

        else if (data.constructor.name === "FormData") {
            //console.log(data.constructor.name)
            data.append("csrfToken", config.csrfToken);
        }

        else if (typeof (data) === "object") {
            //console.log(data.constructor.name)
            data.csrfToken = config.csrfToken;
        }

        return data;
    },
    /**
     * Cette fonction est utilisée pour rediriger.
     *
     * @param string location
     */
    redirectTo: function (location) {
        window.location.href = location;
    },
    /**
     * Verification si la chaine est du JSON
     *
     * @param  XMLHttpRequest  jqXHR
     * @see http://stackoverflow.com/questions/4387688/replace-current-page-with-ajax-content
     */
    IsJsonString: function (str) {
        if(str !== undefined && str !== null && str.constructor == Object){
            return true
        }
        try {
            JSON.parse(str);
        } catch (e) {
            return false;
        }
        return true;
    },
    /**
     * Parse le dernier message lors des Appels SSE en JSON 
     *
     * @param  StrMessage  jqXHR
     */
    parseSSE: function (StrMessage) {
        // -- Recuperation des messages dans un array 
        tmp = StrMessage.split("\n\n###\n\n");

        //console.log(tmp)
        // -- Suppression des valeurs vides
        tmp = tmp.filter(v => v != '');
        //console.log(tmp)
        // -- Inversion du tableau et Recuperation du dernier element
        tmp = tmp.reverse()[0]
        //console.log(tmp)
        // -- Suppression de la chaine "data: "
        tmp = tmp.replace("data: ", "")
        // -- Transformation en Object
        if (helpers.IsJsonString(tmp)) {
            return JSON.parse(tmp)
        } else {
            return {
                date: moment().format("YYYY-MM-DD HH:mm:ss"),
                task: "PROBLEME",
                titre: "Erreur lors du formatage du message SSE",
                progress: 100,
                type: "ERROR",
                message: "Erreur lors du formatage du message SSE"
            }
        }
    },
    
    

    /**
     * Modification de la progress Bar
     *
     * @param  percent  Message
     * @param  reference  id du <div> de la progressBar
     */
    changeProgress: function (message, reference) {
        // -- Modification ProgressBar 
        if ($(reference).length == 0) {
            console.log("L'element DOM " + reference + " n'existe pas")
            return
        }
        // Verification si perc dans objet JSON
        if ((("perc" in message)==true) && message.perc !== null ) {
            $("#progress-bar-modal").width(message.perc + "%").attr('aria-valuenow', message.perc.toString());
            $('#progress-percent-modal').html(message.perc + " %")
            $('#progress-oper-modal').html(message.oper)
        }

    },
}

// =============================================================================================
// AJAX 
// =============================================================================================
// TYPE 	>> Fonction ajax par défaut.
// AUTEUR	>> Julien DENIS Chef de projet ORANGE - UPR Ouest
// CREATION	>> 28/12/2019
// DESCRIPTION  >> Aide appel AJAX
// =============================================================================================

var ajax = {
    /**
    * Fonction ajax par défaut.
    *
    * @param URL        pour envoyer un appel ajax
    * @param données    postData mixtes qui seront envoyées au serveur 
    * @param function   callback Fonction de rappel qui sera appelée en cas de succès ou d'échec
    *
    */
    send: function (url, postData, callback = null, buttonReference = null) {
        var spinnerEle = null;
        $.ajax({
            //headers: {
            //    'Accept': 'application/json',
            //    'Content-Type': 'application/json'
            //},
            url: config.root + url,
            type: "POST",
            data: helpers.appendCsrfToken(postData),
            dataType: "json",
            //processData: false,
            //contentType: false,
            beforeSend: function () {
                // -- Lancement du loader
                app.startLoader('body')
            }
        }).done(function (response) {
            console.log(response)
            if (response.silent == false){
                switch (response.cat) { 
                    case "SUCCESS": 
                        notify.success(response)
                        break;
                    case "ERROR": 
                        notify.error(response)
                        break;
                    case "INFO": 
                        notify.info(response)
                        break;
                    case "DOWNLOAD":
                        helpers.redirectTo(config.root + "files/download/" + response.data)
                        break;
                    case "WARNING": 
                        notify.warning(response)
                        break;
                    default:
                        notify.error( { "mess": "Categorie de message Inconnu : " + response.cat, "oper" : " Traitement reponse AJAX " } )
                }
            }
            // -- Traitement du callback si succes
            if (callback !== null && response.cat == "SUCCESS") {
                eval(callback)
            }


        }).fail(function (response) {
            switch (response.status) { 
                case 400: // Mauvaise Requete
                    notify.error(response.responseJSON)
                    break;
                case 401: // Non-Connecte
                    notify.error(response.responseJSON)
                    break;
                case 403: // Interdit
                    notify.error(response.responseJSON)
                    break;
                case 404: // Mauvaise Route
                    notify.error(response.responseJSON)
                    break;
                case 405: // Mauvaise Requete + CSRF Reject
                    notify.error(response.responseJSON)
                    break;
                case 500: // Exception
                    notify.error(response.responseJSON)
                    break;
                case 302:
                    helpers.redirectTo(config.root);
                    break;
                default:
                    console.log(response.status)
                    console.log(response)
            }
        }).always(function () {
            // -- Fin du loader
            app.stopLoader('body')
        });
    },

}
// =============================================================================================
// AJAX (Server - Sent - Event)
// =============================================================================================
// TYPE 	>> Fonction ajax par avec SSE.
// AUTEUR	>> Julien DENIS Chef de projet ORANGE - UPR Ouest
// CREATION	>> 28/12/2019
// DESCRIPTION  >> Aide appel AJAX
// =============================================================================================
var ajaxSSE = {
        /**
       * Fonction ajax avec Server Sent Event
       *
       * @param URL        pour envoyer un appel ajax
       * @param données    postData mixtes qui seront envoyées au serveur 
       * @param Boolean    useModal Si vous voulez utilisez la fenetre Modal
       * @param function   callback Fonction de rappel qui sera appelée en cas de succès ou d'échec
       *
       */
      send: function (url, postData, callback = null) {
        var refTitre = "#progress-title-modal";
        var refPercent = "#progress-percent-modal";
        var refOper = "#progress-oper-modal"
        var refProgressBar = "#progress-bar-modal";
        var refLog = "#progress-txt-modal";

        $.ajax({
            url: config.root + url,
            type: "POST",
            data: helpers.appendCsrfToken(postData),
            //dataType: "text",
            dataType: "text",
            contentType : "application/json",
            processData: false,
            contentType: false,
            beforeSend: function (jqXHR, settings) {
                // -- Affichage de la modale
                app.showModalLoader()

                // -- Initialisation
                var self = this;
                var xhr = settings.xhr;
                settings.xhr = function () {
                    var output = xhr();
                    output.onreadystatechange = function () {
                        if (typeof (self.readyStateChanged) == "function") {
                            self.readyStateChanged(this);
                        }
                    };
                    return output;
                };
            },
            // -- Ecoute les readyStates
            readyStateChanged: function (jqXHR) {
                console.log("---------------------------------------------------------")
                console.log("State : " + jqXHR.readyState)
                console.log("Status : " + jqXHR.status)
                // -- LOADING  = 3 => la réponse est en cours de chargement (une donnée emballée est reçue)
                if (jqXHR.readyState == 3 && jqXHR.status == 200) {
                    // Changement du titre
                    $(refTitre).html('<i class="fas fa-cogs"></i>&nbspDéroulement des Opérations');
                    // -- Parse du Message
                    message = helpers.parseSSE(jqXHR.responseText)
                    console.log("Message")
                    console.log(message)
                    // -- UPDATE de la tache
                    $(refOper).html(message.titre);
                    // -- UPDATE des logs
                    ajaxSSE.log(message, refLog)
                    // -- UPDATE progression
                    helpers.changeProgress(message, refProgressBar, 100)
                    // -- Auto Scroll
                    $("#log-container").scrollTop($(refLog).height())
                }
            },

        })
        // Fin de la requete avec SUCCES
        .done(function (text, status) {
                // -- Formattage du dernier Message ou renvoi du message JSON
                console.log(text)
                console.log(helpers.IsJsonString(text))
                if(helpers.IsJsonString(text) == true){
                    message = text
                }else{
                    message = helpers.parseSSE(text)
                }
                
                // -- Si le dernier message est de type SUCCESS, on lance le callback si il y en a un
                if(message.cat == 'SUCCESS'){
                    // -- Changement du titre
                    $(refTitre).html('<span class="text-info"><i class="fas fa-check-circle"></i>&nbspTraitement OK</span>');
                    if(callback !== null){
                        //app.closeModalLoader()
                        eval(callback)
                    }
                }
                if(message.cat == 'ERROR'){
                    $(refTitre).html('<span class="text-danger"><i class="fas fa-skull-crossbones"></i>&nbspEchec Traitement</span>');
                }
                if(message.cat == 'WARNING'){
                    $(refTitre).html('<span class="text-warning"><i class="fas fa-comment-medical"></i>&nbspTraitement Impossible</span>');
                    // -- Affichage du message
                    $(refOper).html(message.oper);
                    // -- UPDATE des logs
                    //ajaxSSE.log(message, refLog)
                }
                if(message.cat == 'DOWNLOAD'){
                    // Fermeture du Modal
                    app.closeModalLoader()
                    console.log(message)
                    // Redirection vers le fichier
                    if( message.data !== null && message.data.trim().length > 0){
                        helpers.redirectTo(config.root + "files/download/" + message.data)
                    }else{
                        notify.error({"mess":"Le nom du Fichier à telecharger est inconnu", "oper": "Redirection Telechargement"})
                    }
                    
                }
            })
            // Fin de la requete avec ERREUR
            .fail(function (jqXHR, status) {
                console.log("why")
                
                // -- Parse du Message
                message = helpers.parseSSE(jqXHR.responseText)
                console.log("Message")
                console.log(message)
                // -- Changement du Titre
                $(refTitre).html('<span class="text-danger"><i class="fas fa-skull-crossbones"></i>&nbspTraitement Terminé</span>');

                // -- UPDATE de la tache
                $(refOper).html(message.oper);
                
                if (("perc" in message) == false) {
                    // -- UPDATE des logs
                    ajaxSSE.log(message, refLog)
                }
                //alert("ERREUR")
                //app.closeModalLoader()
                //response = JSON.parse(jqXHR.responseText)
                //notify.error(response)
                //console.log(jqXHR)
            })
            // Sera réalisé si erreur ou pas
            .always(function (text, status) {
                // -- Deblocage du bouton
                $( '#btn-close' ).prop("disabled", false);
                $( "#btn-close" ).removeClass( "d-none" );
                // -- Auto Scroll
                $("#log-container").scrollTop($(refLog).height())
            });
    },
    /**
     * Ajout du message dans le div accueillant les logs
     *
     * @param  message  Objet message
     * @param  reference  id du <div> ou mettre les logs
     */
    log: function (message, reference) {
        if ((("date" in message)==false) || message.date == null ) {
            message.date = moment().format("ddd Do MMM YYYY H:mm:ss")
        }

        // -- Construction du texte
        text = ""
        text += "<div class='row'>"
        text += "   <div class='col-lg-12 col-md-12 col-sm-12 text-left'>"
        // -- Categorie
        switch(message.cat){
            case 'INFO':
                text += "       <span class='float-md-left'>" + message.date + "&nbsp : &nbsp<span class='text-info'>" + message.mess + "</span></span>"
                break;
            case 'SUCCESS':
                text += "       <span class='float-md-left'>" + message.date + "&nbsp : &nbsp<span class='text-success'>" + message.mess + "</span></span>"
                break;
            case 'ERROR':
                text += "       <span class='float-md-left'>" + message.date + "&nbsp : &nbsp<span class='text-danger font-weight-bold'>" + message.mess + "</span></span>"
                break;
            case 'WARNING':
                text += "       <span class='float-md-left'>" + message.date + "&nbsp : &nbsp<span class='text-warning'>" + message.mess + "</span></span>"
                break;
            case 'NORMAL':
                text += "       <span class='float-md-left'>" + message.date + "&nbsp : &nbsp<span class='text-primary'>" + message.mess + "</span></span>"
                break;
            case 'TITLE':
                text += "       <span class='float-md-left'>" + message.date + "&nbsp : &nbsp<span class='text-secondary font-weight-bold'>" + message.mess + "</span></span>"
                break;
            case 'CRITICAL':
                text += "       <span class='float-md-left'>" + message.date + "&nbsp : &nbsp<u><span class='text-danger font-weight-bold'>" + message.mess + "</span></u></span>"
                break;
            case 'DOWNLOAD':
                text += "       <span class='float-md-left'>" + message.date + "&nbsp : &nbsp<span class='font-weight-bold'>" + message.mess + "</span></span>"
                break;
            case 'ERROR_TASK':
                text +="<span class='float-md-left'>" + message.date + "&nbsp : &nbsp<span class='text-dark'>" + message.mess + "</span></span>"
                text +="<span class='float-md-right badge badge-danger'>ECHEC</span>"
                break;
            case 'SUCCESS_TASK':
                text +="<span class='float-md-left'>" + message.date + "&nbsp : &nbsp<span class='text-dark'>" + message.mess + "</span></span>"
                text +="<span class='float-md-right badge badge-success'>SUCCES</span>"
                break;
            default:
                text += "       <span class='float-md-left'>" + message.date + "&nbsp : &nbsp<span class='text-primary font-weight-lighter'>" + message.mess + "</span></span>"
                break;
        }
        text += "</div>"
        text += "</div>"
        // -- Append du message si loader-txt est existant
        if ($(reference).length > 0) {
            // -- Ajout du text
            $(reference).append(text);
            // -- Auto Scroll
            $("#log-container").scrollTop($("#log-container").height())
            //$(reference).append(text).scrollTop($(reference).height());
        } 


        /*
        if (message.type == 'SUCCESS') {
            text += "       <span class='float-md-left'><strong>" + message.date + "</strong>&nbsp : &nbsp<span class='text-success'>" + message.mess + "</span></span>"
        }
        else if (message.type == 'WARNING') {
            text += "       <span class='float-md-left'><strong>" + message.date + "</strong>&nbsp : &nbsp<span class='text-warning'>" + message.mess + "</span></span>"
        }
        else if (message.type == 'ERROR') {
            text += "       <span class='float-md-left'><strong>" + message.date + "</strong>&nbsp : &nbsp<span class='text-danger'>" + message.mess + "</span></span>"
        }
        else if (message.type == 'INFO') {
            text += "       <span class='float-md-left'><strong>" + message.date + "</strong>&nbsp : &nbsp<span class='text-muted'>" + message.mess + "</span></span>"
        }
        else{
            text += "       <span class='float-md-left'><strong>" + message.date + "</strong>&nbsp : &nbsp<span class='font-weight-bold'>" + message.mess + "</span></span>"
        }
        text += "   </div>"
        text += "</div>"
        */
    }

}

// =============================================================================================
// AJAX (Server - Sent - Event)
// =============================================================================================
// TYPE 	>> Fonction ajax par avec SSE.
// AUTEUR	>> Julien DENIS Chef de projet ORANGE - UPR Ouest
// CREATION	>> 28/12/2019
// DESCRIPTION  >> Aide appel AJAX
// =============================================================================================
var ajaxUpload = {
    send: function (url, postData, callback = null) {
        $.ajax({
            url: config.root + url,
            type: 'post',
            data: helpers.appendCsrfToken(postData),
            contentType: false,
            processData: false,
            /*
            success: function(response){
                if(response != 0){
                    $("#img").attr("src",response); 
                    $(".preview img").show(); // Display image element
                }else{
                    alert('file not uploaded');
                }
            },
            */
        }).done(function (response) {
            console.log(response)
            if (response.silent == false){
                switch (response.cat) { 
                    case "SUCCESS": 
                        notify.success(response)
                        break;
                    case "ERROR": 
                        notify.error(response)
                        break;
                    case "INFO": 
                        notify.info(response)
                        break;
                    case "DOWNLOAD":
                        helpers.redirectTo(config.root + "files/download/" + response.data)
                        break;
                    case "WARNING": 
                        notify.warning(response)
                        break;
                    default:
                        notify.error( { "mess": "Categorie de message Inconnu : " + response.cat, "oper" : " Traitement reponse AJAX " } )
                }
            }
            // -- Traitement du callback si success
            if (callback !== null && response.cat == "SUCCESS" ) {
                eval(callback)
            }


        }).fail(function (response) {
            switch (response.status) { 
                case 400: // Mauvaise Requete
                    notify.error(response.responseJSON)
                    break;
                case 401: // Non-Connecte
                    notify.error(response.responseJSON)
                    break;
                case 403: // Interdit
                    notify.error(response.responseJSON)
                    break;
                case 404: // Mauvaise Route
                    notify.error(response.responseJSON)
                    break;
                case 405: // Mauvaise Requete + CSRF Reject
                    notify.error(response.responseJSON)
                    break;
                case 500: // Exception
                    notify.error(response.responseJSON)
                    break;
                case 302:
                    helpers.redirectTo(config.root);
                    break;
                default:
                    console.log(response.status)
                    console.log(response)
            }
        }).always(function () {
            // -- Fin du loader
            app.stopLoader('body')
        })
        
    }

}
