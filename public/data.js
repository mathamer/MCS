
function RefreshFileList(){
    fetch('/api/files/list')
        .then(response => response.json())
        .then(data => {
            let fileListElement = document.getElementById("FileList");
            fileListElement.innerHTML = ""

            data.map(filename => {
                fileListElement.appendChild(GenerateFileListChild(filename))
            })
        });
}


function GenerateFileListChild(filename){
    let listItem = document.createElement("li")
    let child = document.createElement("button")
    let remove = document.createElement("button")
    let link = document.createElement("a")


    link.setAttribute("href", `/api/files/${filename}`)
    link.innerHTML = filename

    remove.setAttribute("onclick", `RemoveFilename("${filename}")`)
    remove.innerHTML = "-"
    remove.setAttribute("class", "BUTTON_STOP SpaceingSmall")

    child.appendChild(link)
    child.setAttribute("class", "BUTTON_START SpaceingSmall")
    
    // child.setAttribute("onclick", `DownloadFilename(${filename})`)
    
    listItem.appendChild(child)
    listItem.appendChild(remove)
    return listItem
}

function DownloadFilename(filename){
    fetch(`/api/files/${filename}`)
}

function RemoveFilename(filename){
    fetch(`/api/files/${filename}/remove`)
    RefreshFileList()
}

RefreshFileList()