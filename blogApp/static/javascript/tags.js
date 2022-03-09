let tags = [];

function removeTag(element, tagName) {
    index = tags.indexOf(tagName);
    tags.splice(index, 1);
    element.remove();
    let resStr = '';
    tags.forEach(tag => {
        resStr = resStr.concat(tag);
        resStr = resStr.concat(' ');
    });
    real_input.value = resStr;
}

function createTag() {
    ul.querySelectorAll("li").forEach(li => {
        li.remove();
    })
    let resStr = '';
    tags.forEach(tag => {
        let liTag = `<li onclick = "removeTag(this, '${tag}')">${tag}</li>`;
        ul.insertAdjacentHTML("beforeend", liTag);
        resStr = resStr.concat(tag);
        resStr = resStr.concat(' ');
    });
    real_input.value = resStr;
}

const input = document.getElementById('js-target');
const real_input = document.getElementsByClassName('hidden-input')[0];
const post_btn = document.getElementById('post');
const ul = document.getElementById('tags-list');

const form = document.getElementsByClassName('blogInput')[0];

function addToList(){
    ul.querySelectorAll("li").forEach(tag=>{
        tags.push(tag.innerText);
    })
}

function connect(e){
    if(e.target.value.slice(-1)==' '){
        let tag = e.target.value;
        if (tag.length > 2 && !tags.includes(tag.slice(0, -1))) {
            tags.push(tag.slice(0, -1));
            createTag();
        }
        input.value = '';
    }
}
window.onload = addToList;

function updateTags(){
    createTag();
}

input.addEventListener("input", connect);
form.addEventListener('submit', updateTags)



