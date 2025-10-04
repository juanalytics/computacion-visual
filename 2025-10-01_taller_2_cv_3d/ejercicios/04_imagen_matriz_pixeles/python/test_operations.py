"""
Test script to show what each matrix operation does
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

def create_test_image():
    """Create a simple test image to understand operations"""
    # Create a 400x600 image with different colored regions
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Add colored rectangles
    img[50:150, 50:200] = [255, 0, 0]    # Red rectangle
    img[50:150, 250:400] = [0, 255, 0]   # Green rectangle  
    img[200:300, 50:200] = [0, 0, 255]   # Blue rectangle
    img[200:300, 250:400] = [255, 255, 0] # Yellow rectangle
    
    # Add some text
    cv2.putText(img, "ORIGINAL", (200, 350), 
               cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    return img

def demonstrate_operations():
    """Show what each operation does step by step"""
    # Create test image
    original = create_test_image()
    
    # Convert BGR to RGB for matplotlib
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    
    # Operation 1: Red region (slicing)
    img1 = original_rgb.copy()
    region1 = img1[100:200, 150:300]  # Select region
    region1[:, :] = [255, 0, 0]       # Make it red
    result1 = img1
    
    # Operation 2: Copy and paste
    img2 = original_rgb.copy()
    source_region = img2[50:150, 50:150]  # Copy this region
    img2[250:350, 250:350] = source_region  # Paste it here
    result2 = img2
    
    # Operation 3: Blur region
    img3 = original_rgb.copy()
    region3 = img3[200:300, 200:400]  # Select region
    region3_blurred = cv2.GaussianBlur(region3, (15, 15), 0)
    img3[200:300, 200:400] = region3_blurred  # Replace with blurred version
    result3 = img3
    
    # Operation 4: Masked operation
    img4 = original_rgb.copy()
    mask = np.zeros(img4.shape[:2], dtype=np.uint8)
    cv2.circle(mask, (300, 200), 80, 255, -1)  # Create circular mask
    img4[mask == 255] = [0, 255, 0]  # Make masked area green
    result4 = img4
    
    # Create visualization
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Matrix Operations Explained', fontsize=16, fontweight='bold')
    
    # Original
    axes[0, 0].imshow(original_rgb)
    axes[0, 0].set_title('1. Original Image\n(400x600 with colored rectangles)', fontsize=12)
    axes[0, 0].axis('off')
    
    # Red region
    axes[0, 1].imshow(result1)
    axes[0, 1].set_title('2. Red Region Operation\nSlicing: img[100:200, 150:300] = RED\n(Direct pixel manipulation)', fontsize=12)
    axes[0, 1].axis('off')
    
    # Copy paste
    axes[0, 2].imshow(result2)
    axes[0, 2].set_title('3. Copy & Paste\nCopy region [50:150, 50:150]\nPaste to [250:350, 250:350]', fontsize=12)
    axes[0, 2].axis('off')
    
    # Blur region
    axes[1, 0].imshow(result3)
    axes[1, 0].set_title('4. Blur Region\nApply Gaussian blur to [200:300, 200:400]\n(Selective filtering)', fontsize=12)
    axes[1, 0].axis('off')
    
    # Masked operation
    axes[1, 1].imshow(result4)
    axes[1, 1].set_title('5. Masked Operation\nCircular mask at (300,200)\nMake masked area GREEN', fontsize=12)
    axes[1, 1].axis('off')
    
    # Hide last subplot
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('../resultados/operations_explained.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("="*60)
    print("MATRIX OPERATIONS EXPLAINED:")
    print("="*60)
    print("1. RED REGION: Demonstrates slicing - selecting a rectangular area")
    print("   and changing all pixels in that region to red.")
    print("   Code: region = img[100:200, 150:300]; region[:, :] = [255, 0, 0]")
    print()
    print("2. COPY & PASTE: Shows how to copy one region and paste it elsewhere.")
    print("   Code: source = img[50:150, 50:150]; img[250:350, 250:350] = source")
    print()
    print("3. BLUR REGION: Applies a filter only to a specific region.")
    print("   Code: region = img[200:300, 200:400]; region = cv2.GaussianBlur(region, ...)")
    print()
    print("4. MASKED OPERATION: Uses a mask to apply changes only to certain pixels.")
    print("   Code: mask = circle; img[mask == 255] = [0, 255, 0]")
    print("="*60)

if __name__ == "__main__":
    demonstrate_operations()
