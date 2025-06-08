import os
import numpy as np
from pathlib import Path

def save_poses_to_txt(image_names, final_poses, output_dir="poses"):
    """
    각 이미지에 대응하는 카메라 포즈를 개별 txt 파일로 저장
    
    Args:
        image_names: 이미지 파일 경로 리스트
        final_poses: 각 이미지에 대응하는 4x4 pose 행렬 리스트
        output_dir: 포즈 파일을 저장할 디렉토리
    """
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 전체 포즈 정보를 하나의 파일에도 저장 (선택사항)
    all_poses_file = os.path.join(output_dir, "all_poses.txt")
    
    with open(all_poses_file, 'w') as f_all:
        f_all.write(f"# Total poses: {len(final_poses)}\n")
        f_all.write("# Format: image_name pose_file_path\n\n")
        
        for i, (image_name, pose) in enumerate(zip(image_names, final_poses)):
            # 이미지 파일명에서 확장자 제거하고 포즈 파일명 생성
            image_basename = os.path.basename(image_name)
            image_stem = os.path.splitext(image_basename)[0]
            pose_filename = f"{image_stem}_pose.txt"
            pose_filepath = os.path.join(output_dir, pose_filename)
            
            # 개별 포즈 파일 저장
            save_single_pose(pose, pose_filepath, image_name)
            
            # 전체 목록 파일에 기록
            f_all.write(f"{image_name} {pose_filepath}\n")
            
    print(f"Saved {len(final_poses)} pose files to {output_dir}/")
    return output_dir

def save_single_pose(pose, filepath, image_name=None):
    """
    단일 포즈 행렬을 txt 파일로 저장
    
    Args:
        pose: 4x4 numpy array (c2w transformation matrix)
        filepath: 저장할 파일 경로
        image_name: (선택) 연관된 이미지 파일명
    """
    with open(filepath, 'w') as f:
        # 헤더 정보
        f.write("# Camera-to-World (c2w) transformation matrix\n")
        if image_name:
            f.write(f"# Image: {image_name}\n")
        f.write("# Format: 4x4 matrix (rotation and translation)\n\n")
        
        # 4x4 행렬 저장
        for row in pose:
            f.write(' '.join([f"{val:.8f}" for val in row]) + '\n')
        
        # 추가 정보 (디버깅용)
        f.write("\n# Camera position (world coordinates):\n")
        camera_pos = pose[:3, 3]
        f.write(f"# x: {camera_pos[0]:.6f}, y: {camera_pos[1]:.6f}, z: {camera_pos[2]:.6f}\n")
        
        # 카메라 방향 (viewing direction = -Z axis)
        viewing_dir = -pose[:3, 2]
        f.write("\n# Viewing direction:\n")
        f.write(f"# x: {viewing_dir[0]:.6f}, y: {viewing_dir[1]:.6f}, z: {viewing_dir[2]:.6f}\n")

def load_pose_from_txt(filepath):
    """
    txt 파일에서 포즈 행렬 읽기
    
    Args:
        filepath: 포즈 파일 경로
        
    Returns:
        4x4 numpy array
    """
    pose = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # 주석이나 빈 줄 건너뛰기
            if line.startswith('#') or not line:
                continue
            # 숫자가 있는 줄만 파싱
            try:
                row = [float(x) for x in line.split()]
                if len(row) == 4:  # 4x4 행렬의 한 행
                    pose.append(row)
            except ValueError:
                continue
    
    return np.array(pose)

def save_poses_compact(image_names, final_poses, output_file="poses_all.txt"):
    """
    모든 포즈를 하나의 파일에 컴팩트하게 저장
    
    Args:
        image_names: 이미지 파일 경로 리스트
        final_poses: 각 이미지에 대응하는 4x4 pose 행렬 리스트
        output_file: 출력 파일 경로
    """
    with open(output_file, 'w') as f:
        f.write(f"# Number of poses: {len(final_poses)}\n")
        f.write("# Format: image_path followed by 4x4 c2w matrix\n\n")
        
        for image_name, pose in zip(image_names, final_poses):
            f.write(f"IMAGE: {image_name}\n")
            for row in pose:
                f.write(' '.join([f"{val:.8f}" for val in row]) + '\n')
            f.write("\n")
    
    print(f"Saved all poses to {output_file}")

# # 사용 예시
# if __name__ == "__main__":
#     # 가정: image_names와 final_poses가 준비되어 있음
#     image_names, depth_image_names = self.get_image_dirs(self.dataset_path)
#     final_poses = self.final_pose
    
#     # 방법 1: 각 포즈를 개별 파일로 저장
#     save_poses_to_txt(image_names, final_poses, output_dir="poses_individual")
    
#     # 방법 2: 모든 포즈를 하나의 파일에 저장
#     save_poses_compact(image_names, final_poses, "poses_all.txt")
    
#     # 저장된 포즈 읽기 테스트
#     test_pose = load_pose_from_txt("poses_individual/image_000_pose.txt")
#     print("Loaded pose shape:", test_pose.shape)