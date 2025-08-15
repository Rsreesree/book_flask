let books = JSON.parse(localStorage.getItem("books")) || [];
const bookList = document.getElementById("book-list");
const popup = document.getElementById("popup");

document.getElementById("addBtn").onclick = () => {
  popup.classList.remove("hidden");
};

function closePopup() {
  popup.classList.add("hidden");
}

function saveBook() {
  const title = document.getElementById("title").value;
  const author = document.getElementById("author").value;

  if (title && author) {
    books.push({ title, author });
    localStorage.setItem("books", JSON.stringify(books));
    renderBooks();
    closePopup();
  }
}

function renderBooks() {
  bookList.innerHTML = "";
  books.forEach((book, index) => {
    const div = document.createElement("div");
    div.textContent = `${book.title} by ${book.author}`;
    const delBtn = document.createElement("button");
    delBtn.textContent = "Delete";
    delBtn.onclick = () => {
      books.splice(index, 1);
      localStorage.setItem("books", JSON.stringify(books));
      renderBooks();
    };
    div.appendChild(delBtn);
    bookList.appendChild(div);
  });
}
