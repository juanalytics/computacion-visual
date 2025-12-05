using UnityEngine;

public class IKRigController : MonoBehaviour
{
    [SerializeField] private Animator animator;
    [SerializeField] private Transform rightHandTarget;
    [SerializeField] private Transform rightHandHome;
    [SerializeField] private float blendSpeed = 4f;

    private float _rightWeight;
    private float _targetWeight;
    private Transform _currentTarget;

    private void Reset()
    {
        animator = GetComponent<Animator>();
    }

    public void SetPose(string pose)
    {
        if (pose == "reach")
        {
            _currentTarget = rightHandTarget;
            _targetWeight = 1f;
        }
        else
        {
            _currentTarget = rightHandHome != null ? rightHandHome : null;
            _targetWeight = 0f;
        }
    }

    private void OnAnimatorIK(int layerIndex)
    {
        if (animator == null) return;

        _rightWeight = Mathf.MoveTowards(_rightWeight, _targetWeight, Time.deltaTime * blendSpeed);
        animator.SetIKPositionWeight(AvatarIKGoal.RightHand, _rightWeight);
        animator.SetIKRotationWeight(AvatarIKGoal.RightHand, _rightWeight);

        if (_currentTarget != null)
        {
            animator.SetIKPosition(AvatarIKGoal.RightHand, _currentTarget.position);
            animator.SetIKRotation(AvatarIKGoal.RightHand, _currentTarget.rotation);
        }
    }
}

