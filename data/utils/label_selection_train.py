import pandas as pd
import os
import shutil 


def select_train_labels(n=5, csv_path=""):
    # TODO: When train data is downloaded, we need to get list of ids downloade
    full_train_data = pd.read_csv(csv_path)
    # Extract only these ids from the full_train_data and perform counting
    
    label_counts = full_train_data.groupby("landmark_id").size().sort_values(ascending=False)

    selected_labels = label_counts.head(n).index.tolist()

    selected_train_data = full_train_data[full_train_data['landmark_id'].isin(selected_labels)]
    selected_train_data.to_csv('selected_train.csv', index=False)
    
    labels_and_count = [(landmark_id, count) for landmark_id, count in label_counts.head(n).items()]

    print(f"Size of selected_train_data: {selected_train_data.shape[0]}")
    print("List of image IDs and their occurrences")
    print(labels_and_count)
    return selected_labels


"""
    Moves selected training images from the src_data_path to dest_data_path
"""
def gather_train_data(train_data="", src_data_path="", dest_data_path=""):
    if not os.path.exists(dest_data_path):
        os.makedirs(dest_data_path)
    
    image_formats = ['.jpg', '.jpeg', '.png']  # Add more image formats if needed
    image_file_paths = []
    
    # Gets list of img ids (names)
    train_data = pd.read_csv(train_data)
    image_ids = set(train_data["id"].tolist())

    for root, dirs, files in os.walk(src_data_path):
        for file in files:
            if file.lower().endswith(tuple(image_formats)):
                file_name = os.path.splitext(file)[0]
                # Ensures that img is within selected pool
                if file_name in image_ids:
                    image_file_paths.append(os.path.join(root, file))
    
    print(f"List of selected train data: {image_file_paths}")

    for image_file_path in image_file_paths:
        # Move the image file to the destination path
        shutil.move(image_file_path, dest_data_path)


def main():
    gather_train_data(src_data_path="/Users/ruipenghan/Desktop/Academics/11. SP 2024/CS 444/project/test", dest_data_path="out")
    # select_train_labels(n=5, csv_path="../labels/train.csv")

if __name__ == '__main__':
    main()