// =============================================================================================
//   _______    _     _      _____        __            _ _   
//  |__   __|  | |   | |    |  __ \      / _|          | | |  
//     | | __ _| |__ | | ___| |  | | ___| |_ __ _ _   _| | |_ 
//     | |/ _` | '_ \| |/ _ \ |  | |/ _ \  _/ _` | | | | | __|
//     | | (_| | |_) | |  __/ |__| |  __/ || (_| | |_| | | |_ 
//     |_|\__,_|_.__/|_|\___|_____/ \___|_| \__,_|\__,_|_|\__|
//                                                            
// =============================================================================================
// NOM 		>> app_default_table
// TYPE 	>> Parametres par default des DataTable
// AUTEUR	>> Julien DENIS Chef de projet ORANGE - UPR Ouest
// CREATION	>> 23/06/2017
// DESCRIPTION  >> Definition des parametres par default 
// =============================================================================================
/**
 * Parametrage de la Table par default
 * @param {type} MESSAGE
 * @returns {undefined}
 */
$.extend(true, $.fn.dataTable.defaults, {
    /* -- --------- -- */
    /* -- GENERALES -- */
    /* -- --------- -- */
    

    "searching": true,
    "paging": false, // Pagination
    "lengthChange": false, // Controle du Nombre d'enregistrements par vue
    "ordering": true, // Autoriser le Sort
    "info": true, // Information en bas de page     
    "fixedHeader": true, // Fixation du Header
    "colReorder": true, // Reordonner les colonnes
    /* -- --------- -- */
    /* --  TOOLBAR  -- */
    /* -- --------- -- */
    buttons: [
        // -- Bouton Refresh

        {
            text: '<i class="fas fa-sync" aria-hidden="true"></i>',
            titleAttr: "Rafraichir les informations",
            className: 'btn btn-default',
            action: function (e, dt, node, config) {
                load('body', 'show');
                //$('#table').DataTable().ajax.reload();
                dt.ajax.reload();
                load('body', 'hidden');
                //window.location.reload(true);
            }
        },
        // -- Bouton Suppression des Filtres
        {
            text: '<i class="fa fa-ban"></i>',
            titleAttr: "Suppression des filtres",
            className: 'btn btn-default',
            action: function (e, dt, node, config) {
                yadcf.exResetAllFilters($('#table').DataTable());
            }
        },
        // -- Bouton Imprimer
        {
            extend: 'print',
            text: '<i class="fa fa-print"></i>',
            titleAttr: "Impression du Document",
            className: 'btn btn-default',
            exportOptions: {
                columns: ':visible',
                format: {
                    header: function (data, row, column, node) {
                        var newdata = data;
                        newdata = newdata.replace(/<.*?<\/*?>/gi, '');
                        newdata = newdata.replace(/<div.*?<\/div>/gi, '');
                        newdata = newdata.replace(/<\/div.*?<\/div>/gi, '');
                        return newdata;
                    }
                }
            },
        },
        // -- Bouton Copier
        {
            extend: 'copy',
            text: '<i class="fa fa-copy"></i>',
            titleAttr: "Copie des Elements dans le presse-papier",
            className: 'btn btn-default',
            key: {
                key: 'c',
                altKey: true
            },
            exportOptions: {
                columns: ':visible',
                format: {
                    header: function (data, row, column, node) {
                        var newdata = data;

                        newdata = newdata.replace(/<.*?<\/*?>/gi, '');
                        newdata = newdata.replace(/<div.*?<\/div>/gi, '');
                        newdata = newdata.replace(/<\/div.*?<\/div>/gi, '');
                        return newdata;
                    }
                }
            },
        },
        // -- Bouton Excel
        {
            extend: 'excel',
            text: '<i class="far fa-file-excel" aria-hidden="true"></i>',
            titleAttr: "Exportation vers Excel",
            className: 'btn btn-default',
            filename: function () {
                var d = new Date();
                var n = d.getTime();
                return 'Export_XLSX_' + n;
            },
            sheetName: 'export',
            messageTop: 'liste',
            customize: function (xlsx) {
                var sheet = xlsx.xl.worksheets['sheet1.xml'];
                var now = new Date();
                var jsDate = now.getDate() + '-' + (now.getMonth() + 1) + '-' + now.getFullYear();
                var user = "SARLA";
                $('c[r=A1] t', sheet).text('Crée le ' + jsDate.toString() + ' par ' + user);
                // -- Mise en forme HEADER
                //Second column
		//$('row c:nth-child(2)', sheet).attr('s', '42');
                
                //All cells
		//$('row c', sheet).attr('s', '25');
                //All cells of row 3 (HEADER)
		$('row c[r^="3"]', sheet).attr('s', '49');
            },

            exportOptions: {
                columns: ':visible',
                format: {
                    header: function (data, row, column, node) {
                        var newdata = data;

                        newdata = newdata.replace(/<.*?<\/*?>/gi, '');
                        newdata = newdata.replace(/<div.*?<\/div>/gi, '');
                        newdata = newdata.replace(/<\/div.*?<\/div>/gi, '');
                        return newdata;
                    }
                }
            },

        },
        // -- Bouton PDF
        {
            extend: 'pdf',
            orientation: 'landscape',
            pageSize: 'A4',
            text: '<i class="far fa-file-pdf" aria-hidden="true"></i>',
            titleAttr: "Exportation vers PDF",
            className: 'btn btn-default',
            header: true,
            //messageTop:'TEST TEST TEST',
            footer: true,
            download: 'open',
            filename: function () {
                var d = new Date();
                var n = d.getTime();
                return 'Export_PDF_' + n;
            },
            exportOptions: {
                columns: ':visible',
                search: 'applied',
                order: 'applied',
                format: {
                    header: function (data, row, column, node) {
                        var newdata = data;

                        newdata = newdata.replace(/<.*?<\/*?>/gi, '');
                        newdata = newdata.replace(/<div.*?<\/div>/gi, '');
                        newdata = newdata.replace(/<\/div.*?<\/div>/gi, '');
                        return newdata;
                    }
                }
            },
            customize: function (doc) {
                //Efface le titre crée par DataTable
                doc.content.splice(0, 1);

                doc.defaultStyle.fontSize = 7;
                doc.styles.tableHeader.fontSize = 7;
                doc.styles.tableHeader.color = 'white';
                doc.styles.tableHeader.fillColor = 'black';
                doc.pageMargins = [20, 60, 20, 30];
                //doc.defaultStyle.alignment = 'center';
                //Creation des variables
                var now = new Date();
                var jsDate = now.getDate() + '-' + (now.getMonth() + 1) + '-' + now.getFullYear();
                //var dateNow = moment().format("ddd Do MMM YYYY") + " " + moment().format("H:mm") + ' (S' + moment().format("WW") + ')';
                var user = "SARLA";

                // Done on http://codebeautify.org/image-to-base64-converter
                var logo = 'data:image/jpeg;base64,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';
                //var logo = 'data:image/jpeg;base64,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ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA=';
                //var logo = getBase64FromImageUrl(url_app + 'public/img/ORANGE_LOGO_rgb.jpeg');
                console.log(logo);
                // Create a header object with 3 columns
                // Left side: Logo
                // Middle: brandname
                // Right side: A document title
                doc['header'] = (function () {
                    return {
                        columns: [
                            {
                                image: logo,
                                width: 24
                            },
                            {
                                alignment: 'left',
                                italics: true,
                                text: 'Orange',
                                fontSize: 18,
                                margin: [10, 0]
                            },
                            {
                                alignment: 'right',
                                fontSize: 14,
                                text: 'liste',
                                //text:'TOTO'
                            }
                        ],
                        margin: 20
                    };
                });
                // Create a footer object with 2 columns
                // Left side: report creation date
                // Right side: current page and total pages
                doc['footer'] = (function (page, pages) {
                    return {
                        columns: [
                            {
                                alignment: 'left',
                                text: ['Creé le : ', {text: jsDate.toString()}, ' par ', {text: user}]
                            },
                            {
                                alignment: 'right',
                                text: ['page ', {text: page.toString()}, ' sur ', {text: pages.toString()}]
                            }
                        ],
                        margin: 20
                    }
                });
                // -- Width 100%
                doc.content[0].table.widths = Array(doc.content[0].table.body[0].length + 1).join('*').split('');
                
                
                var objLayout = {};
                objLayout['hLineWidth'] = function (i) {
                    return .5;
                };
                objLayout['vLineWidth'] = function (i) {
                    return .5;
                };
                objLayout['hLineColor'] = function (i) {
                    return '#aaa';
                };
                objLayout['vLineColor'] = function (i) {
                    return '#aaa';
                };
                objLayout['paddingLeft'] = function (i) {
                    return 4;
                };
                objLayout['paddingRight'] = function (i) {
                    return 4;
                };
                doc.content[0].layout = objLayout;

            }
        },

        // -- Bouton ColVis
        {
            extend: 'colvis',
            text: '<i class="fa fa-cog"></i>',
            titleAttr: "Liste des colonnes",
            className: 'btn btn-default',
        },
        // -- Bouton SaveParam
        /*
        {
            titleAttr: "Sauvegarde de la variante (Visibilité et Ordre)",
            text: '<i class="fa fa-save"></i>',
            className: 'btn btn-default',
            action: function (e, dt, node, config) {
                action_save_param_table();

            }
        }
        */
    ],
    /* -- --------- -- */
    /* --   EVENTS  -- */
    /* -- --------- -- */
    "initComplete": function (settings, json) {

        // -- Parametrage de l'ORDENNACEMENT
        if(param_user !== null){
            if ( (param_user.COL_ORDER !== null) & (param_user.COL_ORDER !== '')) {
                $('#table').DataTable().colReorder.order(param_user.COL_ORDER);
            }
        }
        // -- Parametrage de la VISIBILITE
        if(param_user !== null){
            if ((param_user.COL_VISIBLE !== null) & (param_user.COL_VISIBLE !== '')) {
                $('#table').DataTable().columns().visible(false, false);
                $('#table').DataTable().columns(param_user.COL_VISIBLE).visible(true, true);
                $('#table').DataTable().columns.adjust().draw(false); // adjust column sizing and redraw
            }
        }

        // -- Affichage des buttons
        $('#table').DataTable().buttons().container().appendTo( '#table_wrapper .col-md-6:eq(0)' );
        //table_user_load = true;
        //$('#TableUser').DataTable().buttons().container().appendTo('#TableUser_wrapper .col-sm-6:eq(0)');
        finishload();
    },
    "drawCallback": function (settings, json) {
        //console.log(settings.aiDisplay.length);
        //$('#SpanTotalspan').html(settings.aiDisplay.length);
        $('#SpanTotalGlobale').html(settings.aiDisplay.length);
    },

});





