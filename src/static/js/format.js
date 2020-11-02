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
// FORMATAGE DES INFOS
// =============================================================================================
// TYPE 	    >> Fonctions de Formatage des données
// AUTEUR	    >> Julien DENIS Chef de projet ORANGE - UPR Ouest
// CREATION	    >> 28/12/2019
// DESCRIPTION  >> Liste de Fonctions permettant la mise en page Datable et Autres
// =============================================================================================
var formatDt = {
    /**
     * Formatage d'une taille de base de donnée
     * 
     * @param {*} data la donnée à travailler
     * @param {*} type Le type de filtrage
     * @param {*} row  Toutes les infos pour comparer
     * 
     */
    hmzSize: function (data, type, row) {

        if (type === 'display' || type === 'filter') {
            var thresh = 1 ? 1000 : 1024;
            if(data < thresh) return data + ' B';
            var units = 1 ? ['kB','MB','GB','TB','PB','EB','ZB','YB'] : ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
            var u = -1;
            do {
                data /= thresh;
                ++u;
            } while(data >= thresh);
            return data.toFixed(1)+' '+units[u];
        }
    },
    /**
     * Formatage d'une données Boolean
     * 
     * @param {*} data la donnée à travailler
     * @param {*} type Le type de filtrage
     * @param {*} row  Toutes les infos pour comparer
     * 
     */
    Boolean: function (data, type, row) {
        if (type === 'display' || type === 'filter') {
            switch (data) {
                case '0':
                    //<span id="firstnameInvalid" style="color:red; visibility:hidden">
                    //return '<span class="fas fa-check text-success"></span><span style="visibility:hidden">'+value+'</span>  '; //+ value;
                    return '<span class="fa fa-times text-danger"></span><span style="visibility:hidden">' + data + '</span>'; //+ value;

                    //return  value;
                    break;
                case '1':
                    //return '<span class="glyphicon glyphicon-ok" style="color:limegreen"</span><span style="visibility:hidden">'+value+'</span> '; //+ value;
                    return '<span class="fa fa-check text-success"></span><span style="visibility:hidden">' + data + '</span>'; //+ value;
                    //return  value;
                    break;
                
                case '9':
                        //return '<span class="glyphicon glyphicon-ok" style="color:limegreen"</span><span style="visibility:hidden">'+value+'</span> '; //+ value;
                        return '<span class="fas fa-crown text-warning"></span><span style="visibility:hidden">' + data + '</span>'; //+ value;
                        //return  value;
                        break;
                
                case 0:
                        //<span id="firstnameInvalid" style="color:red; visibility:hidden">
                        //return '<span class="fas fa-check text-success"></span><span style="visibility:hidden">'+value+'</span>  '; //+ value;
                        return '<span class="fa fa-times text-danger"></span><span style="visibility:hidden">' + data + '</span>'; //+ value;
                        //return  value;
                        break;
                case 1:
                        //return '<span class="glyphicon glyphicon-ok" style="color:limegreen"</span><span style="visibility:hidden">'+value+'</span> '; //+ value;
                        return '<span class="fa fa-check text-success"></span><span style="visibility:hidden">' + data + '</span>'; //+ value;
                        //return  value;
                        break;
                case 9:
                        //return '<span class="glyphicon glyphicon-ok" style="color:limegreen"</span><span style="visibility:hidden">'+value+'</span> '; //+ value;
                        return '<span class="fas fa-crown text-warning"></span><span style="visibility:hidden">' + data + '</span>'; //+ value;
                        //return  value;
                        break;
                case 'N':
                    //<span id="firstnameInvalid" style="color:red; visibility:hidden">
                    //return '<span class="fas fa-check text-success"></span><span style="visibility:hidden">'+value+'</span>  '; //+ value;
                    return '<span class="fa fa-times text-danger"><span style="visibility:hidden">' + data + '</span></span>'; //+ value;

                    //return  value;
                    break;
                case 'O':
                    //return '<span class="glyphicon glyphicon-ok" style="color:limegreen"</span><span style="visibility:hidden">'+value+'</span> '; //+ value;
                    return '<span class="fa fa-check text-success"><span style="visibility:hidden">' + data + '</span></span>'; //+ value;
                    //return  value;
                    break;
                case false:
                    //<span id="firstnameInvalid" style="color:red; visibility:hidden">
                    //return '<span class="fas fa-check text-success"></span><span style="visibility:hidden">'+value+'</span>  '; //+ value;
                    return '<span class="fa fa-times text-danger"><span style="visibility:hidden">' + data + '</span></span>'; //+ value;

                    //return  value;
                    break;
                case true:
                    //return '<span class="glyphicon glyphicon-ok" style="color:limegreen"</span><span style="visibility:hidden">'+value+'</span> '; //+ value;
                    return '<span class="fa fa-check text-success"><span style="visibility:hidden">' + data + '</span></span>'; //+ value;
                    //return  value;
                    break;
                default:
                    return data;
            }
        }
    },
    /**
     * Formatage d'une données Boolean
     * 
     * @param {*} data la donnée à travailler
     * @param {*} type Le type de filtrage
     * @param {*} row  Toutes les infos pour comparer
     * 
     */
    isEmptyToBool: function (data, type, row) {
        if (type === 'display' || type === 'filter') {
            if(data == null || data.length == 0){
                return '<span class="fa fa-check text-danger"></span><span style="visibility:hidden">false</span>'; //+ value;
            }else{
                return '<span class="fa fa-check text-success"></span><span style="visibility:hidden">true</span>'; //+ value;
            }
        }
    },
    /**
     * Formatage classique d'un TIMESTAMP
     * 
     * @param {*} data la donnée à travailler
     * @param {*} type Le type de filtrage
     * @param {*} row  Toutes les infos pour comparer
     * 
     */
    TimestampBasicFormatter: function (data, type, row) {
        if (type === 'display' || type === 'filter') {
            if (!moment(data).isValid()) {
                return data;
            }
            console.log(config.timeZone)
            // Definiation du TimeZone
            //var DATE_VAL = moment(data).tz(config.timeZone);
            var DATE_VAL = moment.utc(data) // .tz(config.timeZone)
            //console.log("DIFFERENCE >> " + moment().diff(DATE_VAL, 'days'));
            return DATE_VAL.format("ddd DD MMM YYYY HH:mm:ss");
        }
        // Otherwise the data type requested (`type`) is type detection or
        // sorting value, for which we want to use the integer, so just return
        // that, unaltered
        return data;
    },
    /**
     * Formatage classique d'un TIMESTAMP
     * 
     * @param {*} data la donnée à travailler
     * @param {*} type Le type de filtrage
     * @param {*} row  Toutes les infos pour comparer
     * 
     */
    GpFormatter: function (data, type, row) {
        if ( type === 'display' || type === 'filter' ) {
            // <span class="badge badge-pill badge-success">MAD</span>'
    
            nValue = parseFloat(data);
            if(isNaN(nValue))
                return data
        
            if(nValue > 0){
                return '<span class="text-success">' + nValue + '</span>';
            }
            if(nValue < 0){
                return '<span class="text-danger">' + nValue + '</span>';
            }
            return data
            }
        // Otherwise the data type requested (`type`) is type detection or
        // sorting value, for which we want to use the integer, so just return
        // that, unaltered
        return data;
    },



    /**
     * Formatage classique d'un TIMESTAMP
     * 
     * @param {*} data la donnée à travailler
     * @param {*} type Le type de filtrage
     * @param {*} row  Toutes les infos pour comparer
     * 
     */
    EvalFormatter: function (data, type, row) {
        if ( type === 'display' || type === 'filter' ) {
            // <span class="badge badge-pill badge-success">MAD</span>'
    
            nValue = parseFloat(row['profit']);
            if(isNaN(nValue)){
                return data
            }
            if(nValue > 0){
                return '<i class="fas fa-smile-wink text-success"></i>';
            }
            if(nValue < 0){
                return '<i class="fas fa-angry text-danger"></i>';
            }
            if(nValue == 0){
                return '<i class="fas fa-equals text-warning"></i>';
            }
            return data
            }
        // Otherwise the data type requested (`type`) is type detection or
        // sorting value, for which we want to use the integer, so just return
        // that, unaltered
        return data;
    },
    /**
     * Formatage classique d'un TIMESTAMP
     * 
     * @param {*} data la donnée à travailler
     * @param {*} type Le type de filtrage
     * @param {*} row  Toutes les infos pour comparer
     * 
     */
    DirectionFormatter: function (data, type, row) {
        if ( type === 'display' || type === 'filter' ) {
            // <span class="badge badge-pill badge-success">MAD</span>'
    
            openPrice = parseFloat(row['open_price']);
            TpPrice = parseFloat(row['tp']);
            if(isNaN(openPrice)){
                return '<span class="badge badge-pill badge-warning">???</span>';
            }
            if(isNaN(TpPrice)){
                return '<span class="badge badge-pill badge-warning">???</span>';
            }
            if(openPrice > TpPrice){
                return '<span class="badge badge-pill badge-danger">VENTE</span>';
            }
            if(openPrice < TpPrice){
                return '<span class="badge badge-pill badge-success">ACHAT</span>';
            }
            return data
            }
        // Otherwise the data type requested (`type`) is type detection or
        // sorting value, for which we want to use the integer, so just return
        // that, unaltered
        return data;
    },


}