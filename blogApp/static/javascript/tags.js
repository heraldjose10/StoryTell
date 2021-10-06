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

function addTag(e) {
    if (e.keyCode == 32 || e.key == ',' || e.key == 'Enter') {
        let tag = e.target.value;
        if (tag.length > 2 && !tags.includes(tag.slice(0, -1))) {
            tags.push(tag.slice(0, -1));
            createTag();
        }
        input.value = '';
    }

}


const input = document.getElementById('js-target');
const real_input = document.getElementsByClassName('hidden-input')[0]
const post_btn = document.getElementById('post');
ul = document.getElementsByTagName('ul')[1]


input.addEventListener("keyup", addTag);

post_btn.addEventListener('onclick', inputTags);


