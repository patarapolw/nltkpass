$(() => {
    $("#generate-sentence").click(async () => {
        const {sentence} = await $.post("/api/sentence")
        $("#sentence").text(sentence);
        $("#user-sentence").val(sentence)
        $("#sentence-output").show();
    });

    $("#generate-password").click(async () => {
        $("#password").text((await $.post("/api/password", {
            sentence: $("#user-sentence").val()
        })).password);
    })
});