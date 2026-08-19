# Project
Laboratorio estructural digital 3D del Edificio de Ingeniería.

# Units
SI (N, m, kg, Pa).

# Structural model
- Global model: linear elastic 3D with 6 DOF per node.
- Elements: elasticBeamColumn for beams and columns.
- Walls: equivalent linear elements per course convention.
- Slabs: NOT modeled with FEM. Gravity loads via tributary areas.
- Rigid diaphragms at each floor.
- RC fiber sections are separate from the global model.

# Load cases
- G: self-weight (slab + finishes) + self-weight of structural elements.
- Q: live load.
- EX: lateral load in X.
- EY: lateral load in Y.
- Superposition: R = Σ λᵢ · Rᵢ

# Architecture
- OpenSees / OpenSeesPy owns structural analysis.
- Unity owns visualization / preprocessing / interaction / AR.
- JSON is the contract between both.
- Mobile does NOT run OpenSees in the base project.
- Data formats must exist independently of the Unity scene.

# Verification rules
- Check global equilibrium: ΣF_applied + ΣR ≈ 0.
- Check units in every output.
- Check local axes orientation.
- Check superposition: R(A+B) = R(A) + R(B).
- Check tributary area load conservation: Σ(q·A_trib) = q·A_total.
- Every exported elementTag must exist exactly once in the viewer.
- Never modify reference benchmark results without justification.

# Workflow
- Issue → Plan → Build → Test → Review → Merge
- Each task must have: objective, constraints, acceptance criteria, test, review.

# Agents
- structural-reviewer: DOF, units, axes, supports, equilibrium, loads, superposition, diagrams, RC capacity.
- unity-reviewer: elementTag ↔ GameObject mapping, transforms, scales, JSON I/O, selection, data modification.
- load-path-reviewer: tributary areas, load conservation, polygon-beam association, mobile loads.
- ar-reviewer: image tracking, pose, anchor, scale, coordinate transforms OpenSees → Unity → AR.
- test-planner: proposes tests before implementation.

# Do NOT delegate without review
- Structural idealization choices.
- Local axes meaning.
- Tributary distribution.
- Support definitions.
- Capacity criteria.
- P-M interpretation.
- Mobile load distribution rule (SQ4).
- AR physical alignment.
