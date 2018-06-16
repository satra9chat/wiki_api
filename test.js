function postData(input) {
    var hi = new ajax
    hi.ajax({
        type: "POST",
        url: "/wiki_api.py",
        data: { param: input },
        success: callbackFunc
    });
}

function callbackFunc(response) {
    // do something with the response
    console.log(response);
}

postData("golden retriever","dog");