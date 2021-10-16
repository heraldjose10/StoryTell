const choose_file = document.getElementById('choose-file');

function resize_img(w, h=null){
    const file = choose_file.files[0];

    if(!file){
        console.log("No file");
        return;
    } 

    const reader = new FileReader();

    reader.readAsDataURL(file);
    
    reader.onload = function(e){
        const imgElement = document.createElement("img");
        imgElement.src = e.target.result;
        imgElement.onload = function (event) {
            const canvas = document.createElement("canvas");
            const MAX_WIDTH = w;
            canvas.width = MAX_WIDTH;

            if(h==null){
                const scaleSize = MAX_WIDTH / event.target.width;
                canvas.height = event.target.height * scaleSize;
            }
            else{
                canvas.height = h;
            }
            
      
            const ctx = canvas.getContext("2d");
      
            ctx.drawImage(event.target, 0, 0, canvas.width, canvas.height);
      
            const srcEncoded = ctx.canvas.toDataURL(e.target, "image/jpeg");
      
            // document.getElementById("upload").src = srcEncoded;
            document.getElementById("img_data").value = srcEncoded;
          };
    }
}

// choose_file.onchange = resize_img;