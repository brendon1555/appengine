var oReq;
var band;

function addBand(){

    //create an instance of xhr
    oReq = new XMLHttpRequest();

    //open the url
    oReq.open("POST", "/band");

    //set the request header content-type to json
    oReq.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    //get the the value of the band text input
    band = document.getElementById("band").value;

    oReq.onreadystatechange=function()
    {
        //if the request has finished and the status is OK
        if (oReq.readyState==4 && oReq.status==200)
        {
            //create the list item for the added band
            var li = document.createElement("LI");
            
            li.setAttribute("id", oReq.responseText);

            var litext = document.createTextNode(band);

            var lilink = document.createElement("a");
            lilink.setAttribute("href", "/band/" + oReq.responseText + "/album");

            var linktext = document.createTextNode("See Albums");
            var libutton = document.createElement("button");
            libutton.setAttribute("onclick", "deleteBand(this.id)");

            var buttontext = document.createTextNode("Delete Band");

            li.appendChild(litext);

            lilink.appendChild(linktext);
            li.appendChild(lilink);
            libutton.appendChild(buttontext);
            li.appendChild(libutton);
            document.getElementById("bands").appendChild(li);
        }
    }
    //send the band to the server
    oReq.send(JSON.stringify({'band': band}));
    return false;
}

function addAlbum(){
    //create an instance of xhr
    oReq = new XMLHttpRequest();

    //open the url
    oReq.open("POST", "album");

    //set the request header content-type to json
    oReq.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    //get the value of the album text input
    var album = document.getElementById("album").value;

    //get the name of the band from a div
    var band = document.getElementById("band-name").innerHTML;

    oReq.onreadystatechange=function()
    {
        //if the request has finished and the status is OK
        if (oReq.readyState==4 && oReq.status==200)
        {
            //create the list item for the added album
            var li = document.createElement("LI");
            li.setAttribute("onclick", "deleteAlbum(this.id)");
            li.setAttribute("id", oReq.responseText);
            var litext = document.createTextNode(album + " (Click to delete)");
            li.appendChild(litext);
            document.getElementById("albums").appendChild(li);
        }
    }
    //send the album to the server
    oReq.send(JSON.stringify({ 'album': album, 'band': band }));
    console.log(JSON.stringify({ 'album': album, 'band': band }));
    return false;
}

function deleteBand(id){
    //create an instance of xhr
    oReq = new XMLHttpRequest();

    //open the url
    oReq.open("DELETE", "/band/" + id);

    oReq.onreadystatechange=function()
    {
        //if the request has finished and the status is No Content
        if (oReq.readyState==4 && oReq.status==204)
        {
            //remove the band form the list
            var band_node = document.getElementById(id);
            band_node.parentNode.removeChild(band_node);
        }
    }
    oReq.send();
}

function deleteAlbum(id){
    //create an instance of xhr
    oReq = new XMLHttpRequest();

    //open the url
    oReq.open("DELETE", "album/" + id);

    oReq.onreadystatechange=function()
    {
        //if the request has finished and the status is No Content
        if (oReq.readyState==4 && oReq.status==204)
        {
            //remove the album from the list
            var album_node = document.getElementById(id);
            album_node.parentNode.removeChild(album_node);
        }
    }
    oReq.send();
}