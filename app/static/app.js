const exampleText = "Gostei bastante do fone de ouvido. A cor veio exatamente como descrita (bege), bem bonita. O produto é leve, confortável e dobrável, o que facilita bastante no uso e no transporte. Veio bem embalado e a entrega foi realizada no prazo informado pelo site, conforme combinado. O carregador é apenas um cabo USB tipo C pequeno, não acompanha fonte, o que já é esperado em alguns modelos. O volume é alto e a qualidade do som atende bem. O fone é confortável mesmo em uso prolongado. Como ponto de atenção, antes de conectar ao Bluetooth ele emite um sinal sonoro estranho, parecido com uma TV quando perde o sinal. No começo incomoda um pouco, mas depois passa a não ser mais perceptível. No geral, é um bom produto e atende bem às expectativas pelo valor.";

const form = document.getElementById("summarization-form");
const textInput = document.getElementById("text");
const fileInput = document.getElementById("file");
const sentenceCount = document.getElementById("n_sentences");
const submitButton = document.getElementById("submit-button");
const formMessage = document.getElementById("form-message");
const emptyState = document.getElementById("empty-state");
const summaryText = document.getElementById("summary-text");
const resultContent = document.getElementById("result-content");
const resultCount = document.getElementById("result-count");
const sentenceList = document.getElementById("sentence-list");
const textTab = document.getElementById("text-tab");
const fileTab = document.getElementById("file-tab");
const textSource = document.getElementById("text-source");
const fileSource = document.getElementById("file-source");
let source = "text";

function selectSource(nextSource) {
    source = nextSource;
    const isText = source === "text";
    textTab.setAttribute("aria-pressed", String(isText));
    fileTab.setAttribute("aria-pressed", String(!isText));
    textSource.hidden = !isText;
    fileSource.hidden = isText;
    formMessage.textContent = "";
}

textTab.addEventListener("click", () => selectSource("text"));
fileTab.addEventListener("click", () => selectSource("file"));

document.getElementById("use-example").addEventListener("click", () => {
    selectSource("text");
    textInput.value = exampleText;
    sentenceCount.value = "2";
    textInput.focus();
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    formMessage.textContent = "";

    if (!sentenceCount.validity.valid) {
        sentenceCount.reportValidity();
        return;
    }

    const requestBody = new FormData();
    if (source === "text") {
        if (!textInput.value.trim()) {
            formMessage.textContent = "Digite um texto para resumir.";
            textInput.focus();
            return;
        }
        requestBody.append("text", textInput.value);
    } else {
        const textFile = fileInput.files[0];
        if (!textFile) {
            formMessage.textContent = "Escolha um arquivo .txt.";
            fileInput.focus();
            return;
        }
        if (!textFile.name.toLowerCase().endsWith(".txt")) {
            formMessage.textContent = "Escolha um arquivo .txt.";
            fileInput.focus();
            return;
        }
        requestBody.append("file", textFile);
    }
    requestBody.append("n_sentences", sentenceCount.value);

    submitButton.disabled = true;
    submitButton.textContent = "Resumindo...";

    try {
        const response = await fetch(form.action, { method: "POST", body: requestBody });
        if (!response.ok) {
            formMessage.textContent = "Não foi possível gerar o resumo. Confira a entrada e tente novamente.";
            return;
        }

        const result = await response.json();
        sentenceList.replaceChildren();

        if (!result.sentences.length) {
            summaryText.hidden = true;
            resultContent.hidden = true;
            emptyState.hidden = false;
            formMessage.textContent = "Nenhuma frase foi encontrada no texto.";
            return;
        }

        for (const sentence of result.sentences) {
            const row = document.createElement("li");
            const sentenceText = document.createElement("span");
            const sentenceScore = document.createElement("span");
            row.className = "sentence-row";
            sentenceText.className = "sentence-text";
            sentenceScore.className = "sentence-score";
            sentenceText.textContent = sentence.text;
            sentenceScore.textContent = sentence.score.toFixed(4);
            sentenceScore.setAttribute("aria-label", `Pontuação ${sentence.score.toFixed(4)}`);
            row.append(sentenceText, sentenceScore);
            sentenceList.append(row);
        }

        const count = result.sentences.length;
        resultCount.textContent = `${count} ${count === 1 ? "frase selecionada" : "frases selecionadas"}`;
        summaryText.textContent = result.summary;
        summaryText.hidden = false;
        emptyState.hidden = true;
        resultContent.hidden = false;
    } catch {
        formMessage.textContent = "Não foi possível conectar ao servidor. Tente novamente.";
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Resumir texto";
    }
});
