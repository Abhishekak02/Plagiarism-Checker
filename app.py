import os
from tkinter import Tk, Button, Label, Listbox, Scrollbar, END, SINGLE, Frame
from tkinter.filedialog import askopenfilename
from tkinter.font import Font

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to calculate vector representation of text
def vectorize(text):
    return TfidfVectorizer().fit_transform(text).toarray()

# Function to calculate cosine similarity between two documents
def similarity(doc1, doc2):
    return cosine_similarity([doc1, doc2])

# Function to browse and select files
def browse_files():
    filename = askopenfilename()
    if filename:
        file_listbox.insert(END, filename)

# Function to remove selected files
def remove_files():
    selected_indices = file_listbox.curselection()
    if selected_indices:
        for index in reversed(selected_indices):
            file_listbox.delete(index)

# Function to detect plagiarism
def detect_plagiarism():
    # Retrieve selected files from the listbox
    selected_files = file_listbox.get(0, END)
    if len(selected_files) < 2:
        result_label.config(text="Please select at least 2 files.")
        return
    
    # Read the contents of selected files
    student_notes = [open(file, encoding='utf-8').read() for file in selected_files]
    
    # Vectorize the student notes
    vectors = vectorize(student_notes)
    s_vectors = list(zip(selected_files, vectors))
    plagiarism_results = set()

    # Check for plagiarism
    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1], sim_score)
            plagiarism_results.add(score)

    # Display the plagiarism results
    result_label.config(text="Plagiarism Results:")
    result_listbox.delete(0, END)
    for data in plagiarism_results:
        result_listbox.insert(END, data)

# Create the Tkinter window
window = Tk()
window.title("PlagScan")
window.geometry("400x400")

# Create font
font = Font(family="Arial", size=12)

# Create file selection components
file_frame = Frame(window)
file_frame.pack(pady=10)

file_scrollbar = Scrollbar(file_frame)
file_scrollbar.pack(side="right", fill="y")

file_listbox = Listbox(file_frame, width=50, selectmode=SINGLE, font=font, yscrollcommand=file_scrollbar.set)
file_listbox.pack(side="left", fill="y")

file_scrollbar.config(command=file_listbox.yview)

button_frame = Frame(window)
button_frame.pack(pady=5)

browse_button = Button(button_frame, text="Browse Files", command=browse_files, font=font)
browse_button.pack(side="left", padx=5)

remove_button = Button(button_frame, text="Remove File", command=remove_files, font=font)
remove_button.pack(side="left", padx=5)

detect_button = Button(button_frame, text="Detect Plagiarism", command=detect_plagiarism, font=font)
detect_button.pack(side="left", padx=5)

# Create plagiarism detection components
result_label = Label(window, text="", font=font)
result_label.pack()

result_frame = Frame(window)
result_frame.pack()

result_scrollbar = Scrollbar(result_frame)
result_scrollbar.pack(side="right", fill="y")

result_listbox = Listbox(result_frame, width=50, font=font, yscrollcommand=result_scrollbar.set)
result_listbox.pack(side="left", fill="y")

result_scrollbar.config(command=result_listbox.yview)

# Start the Tkinter event loop
window.mainloop()
