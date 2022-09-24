let width = screen.width;

if (width <= 992) {
    let navitems = document.querySelectorAll(".nav-item");
    let firstNav = document.getElementById("first-nav");
    firstNav.classList.remove("border-start");
    navitems.forEach((e) => {
        e.classList.remove("border-end");
    });
    console.log("it working nav");
}

// ==========Display Download Document Detail===========

function showDocumentDetail(dname, ddescription, dprice) {
    var documentDetails = document.getElementById("document-details"),
        name = document.getElementById("name"),
        description = document.getElementById("description"),
        price = document.getElementById("price");

    documentDetails.classList.remove("d-none");
    name.innerHTML = dname;
    description.innerHTML = ddescription;
    price.innerHTML = dprice;

    console.log("Show Document");
}
