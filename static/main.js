var name = "";
var optionsd = document.get('po');
window.alert(optionsd.length);

for (var i = 0; i <  optionsd.length; i++) {
    window.alert("hitt")
    optionsd[i].addEventListener('click', function () {

        window.alert("hitt")
    })
}


function f(a) {
    name = a;
    document.getElementById("username").innerHTML = name;


    addOption();
}


function f1() {

    window.alert('a')
}

function addOption() {

    var cc = document.createElement('ul');
    var qq = document.createElement('li');
    //qq.textContent("hello");
    qq.innerText = name;
    cc.appendChild(qq);
    var element = document.body;
    var baby = document.getElementById('sss');
    element.insertBefore(qq, baby);
    window.alert('aaa')
    console.log('aaaaaaankjnfjfnwerknewkjenfejkkj')


}

function search_movie() {
    var new_form = document.createElement('form');
    var search_bar = document.createElement('INPUT');
    search_bar.setAttribute("type", "text");
    var search_button = document.createElement('INPUT');
    search_button.setAttribute("type", "submit");
    search_button.setAttribute("value", "search");

    search_bar.setAttribute("content", "option");
     search_bar.setAttribute("name", "option");
    search_button.setAttribute("class", "menu-button");
    search_bar.setAttribute("class", "menu-button");
    new_form.appendChild(search_bar);
    new_form.appendChild(search_button);


    new_form.method = 'POST';
    new_form.action = '/external/';

    var baby = document.getElementById('search_movies');
    baby.parentNode.insertBefore(new_form,baby.nextSibling);


    return false;

}


function rate_move(r) {

    window.alert(r.dataset.movie);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/add_movie/", true);
    xhr.open("POST", "/add_movie/", true);
    xhr.send(JSON.stringify({
    movie: r.dataset.movie,
        rate : r.dataset.rate
}));


}
