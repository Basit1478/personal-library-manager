import streamlit as st
import pandas as pd
import pickle
import os

# ---------- File Handling ---------- #
LIBRARY_FILE = "library.pkl"

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "rb") as f:
            return pickle.load(f)
    return []

def save_library(library):
    with open(LIBRARY_FILE, "wb") as f:
        pickle.dump(library, f)

# ---------- Initialize Session State ---------- #
if 'library' not in st.session_state:
    st.session_state.library = load_library()

# ---------- Helper Functions ---------- #
def add_book(title, author, year, genre, read_status):
    book = {
        "Title": title,
        "Author": author,
        "Year": year,
        "Genre": genre,
        "Read": read_status
    }
    st.session_state.library.append(book)
    save_library(st.session_state.library)
    st.success(f"Book '{title}' added successfully!")

def remove_book(title):
    original_len = len(st.session_state.library)
    st.session_state.library = [book for book in st.session_state.library if book["Title"].lower() != title.lower()]
    if len(st.session_state.library) < original_len:
        save_library(st.session_state.library)
        st.success(f"Book '{title}' removed successfully!")
    else:
        st.warning(f"No book found with title '{title}'.")

def search_books(keyword):
    keyword = keyword.lower()
    results = [
        book for book in st.session_state.library
        if keyword in book["Title"].lower() or keyword in book["Author"].lower()
    ]
    return results

def display_books(books):
    if not books:
        st.info("No books to display.")
        return
    df = pd.DataFrame(books)
    df["Read"] = df["Read"].apply(lambda x: "Yes" if x else "No")
    st.dataframe(df)

def display_statistics():
    total_books = len(st.session_state.library)
    read_books = len([book for book in st.session_state.library if book["Read"]])
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0

    st.subheader("📊 Library Statistics")
    st.write(f"Total Books: **{total_books}**")
    st.write(f"Books Read: **{read_books}**")
    st.write(f"Percentage Read: **{percent_read:.2f}%**")

# ---------- Streamlit UI ---------- #
st.title("📚 Personal Library Manager")

menu = st.sidebar.selectbox("Menu", ["Add a Book", "Remove a Book", "Search Books", "Display All Books", "Statistics"])

if menu == "Add a Book":
    st.header("➕ Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, step=1)
        genre = st.text_input("Genre")
        read_status = st.checkbox("Read", value=False)
        submitted = st.form_submit_button("Add Book")

        if submitted:
            if title and author and genre:
                add_book(title, author, year, genre, read_status)
            else:
                st.warning("Please fill in all required fields.")

elif menu == "Remove a Book":
    st.header("🗑️ Remove a Book")
    title_to_remove = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        if title_to_remove:
            remove_book(title_to_remove)
        else:
            st.warning("Please enter a book title.")

elif menu == "Search Books":
    st.header("🔎 Search for a Book")
    keyword = st.text_input("Enter keyword (Title or Author)")
    if keyword:
        results = search_books(keyword)
        st.subheader(f"Found {len(results)} result(s):")
        display_books(results)

elif menu == "Display All Books":
    st.header("📖 All Books in Your Library")
    display_books(st.session_state.library)

elif menu == "Statistics":
    display_statistics()

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
