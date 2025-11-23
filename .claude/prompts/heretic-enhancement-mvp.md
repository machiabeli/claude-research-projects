# Heretic Enhancement: Research Paper Implementation

> **Optimized Claude Code on the Web Prompt - MVP + Iterative Cycles**
> **Target**: Implement 6 cutting-edge research papers to enhance the heretic model ablation framework
> **Approach**: Comprehensive analysis → MVP implementation → Validation → Iterative improvements

---

## 🎯 Mission

Enhance the [heretic framework](https://github.com/machiabeli/heretic) by implementing techniques from 6 recent research papers to:

1. Improve ablation effectiveness and interpretability
2. Add support for SSM/hybrid architectures (Mamba, Jamba, etc.)
3. Implement advanced steering techniques
4. Enable deeper safety alignment analysis
5. Provide better numerical validation

## 📚 Research Papers to Implement

### Primary Papers (Core Enhancements)

1. **Anthropic Persona Vectors** (arXiv:2507.21509)
   - **URL**: https://arxiv.org/abs/2507.21509
   - **Code**: https://github.com/safety-research/persona_vectors
   - **Focus**: Automated persona vector extraction with natural language descriptions
   - **Impact**: Enhance heretic's harmful/harmless prompt methodology

2. **Self-Ablating Transformers** (arXiv:2505.00509)
   - **URL**: https://arxiv.org/abs/2505.00509
   - **Focus**: Better ablation with less performance degradation
   - **Impact**: Improve heretic's core ablation technique

3. **Representation Engineering Survey** (arXiv:2502.17601)
   - **URL**: https://arxiv.org/abs/2502.17601
   - **Focus**: Contrastive methodology improvements
   - **Impact**: Enhance direction identification

### Advanced Techniques

4. **Steering with Conceptors** (arXiv:2410.16314)
   - **URL**: https://arxiv.org/abs/2410.16314
   - **Focus**: Ellipsoidal region representations
   - **Impact**: Replace simple directional ablation with geometric methods

5. **Safety Alignment Depth** (arXiv:2502.00669)
   - **URL**: https://arxiv.org/abs/2502.00669
   - **Focus**: Layer-specific alignment targeting
   - **Impact**: Enable selective layer ablation

### Architecture Extension

6. **Samba: Hybrid State Space Models** (arXiv:2406.07522)
   - **URL**: https://arxiv.org/abs/2406.07522
   - **Focus**: SSM + Transformer hybrid architecture
   - **Impact**: Add Mamba/Jamba support to heretic

---

## 🏗️ Implementation Strategy

### Phase 1: MVP (First Claude Code on Web Session)

**Objective**: Working baseline with 2-3 paper techniques integrated

**Tasks**:

1. **Environment Setup** ✅
   ```bash
   # Clone your heretic fork
   git clone https://github.com/machiabeli/heretic.git
   cd heretic

   # Create isolated environment
   python3.10 -m venv .venv
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```

2. **Codebase Analysis** 🔍
   - Use `/research-paper-implementation` skill
   - Map heretic's current architecture
   - Identify integration points for new techniques
   - Document current limitations

3. **Paper Implementation Priority** 📖

   **MVP Papers** (Implement these first):
   - ✅ Anthropic Persona Vectors (has reference code!)
   - ✅ Self-Ablating Transformers

   **Rationale**:
   - Persona Vectors has open-source implementation to learn from
   - Self-Ablating directly improves core ablation
   - Both are well-documented and tested

4. **Integration Approach** 🔧

   **Persona Vectors Integration**:
   ```python
   # Add to heretic/direction_finder.py
   class PersonaVectorExtractor:
       """Extract persona vectors using natural language descriptions"""

       def __init__(self, model, tokenizer):
           self.model = model
           self.tokenizer = tokenizer

       def extract_from_description(self, trait_description: str):
           """
           Args:
               trait_description: Natural language (e.g., "evil", "sycophancy")
           Returns:
               persona_vectors: Dict[layer_idx, torch.Tensor]
           """
           # Generate contrastive prompts from description
           positive_prompts = self._generate_positive_prompts(trait_description)
           negative_prompts = self._generate_negative_prompts(trait_description)

           # Extract activations
           pos_acts = self._get_activations(positive_prompts)
           neg_acts = self._get_activations(negative_prompts)

           # Compute directions as difference-of-means
           persona_vectors = {}
           for layer in range(self.model.config.num_hidden_layers):
               persona_vectors[layer] = (
                   pos_acts[layer].mean(dim=0) - neg_acts[layer].mean(dim=0)
               )

           return persona_vectors
   ```

   **Self-Ablating Integration**:
   ```python
   # Enhance heretic/ablation.py
   class SelfAblatingOrthogonalizer:
       """Improved ablation with self-ablation techniques"""

       def orthogonalize_with_self_ablation(
           self,
           weight: torch.Tensor,
           direction: torch.Tensor,
           alpha: float = 1.0
       ):
           """
           Apply self-ablation technique for better interpretability

           Args:
               weight: Model weight matrix
               direction: Refusal direction to remove
               alpha: Ablation strength
           """
           # Compute projection (standard)
           proj = torch.outer(direction, direction) / (direction.norm()**2)

           # Self-ablation enhancement: gradual removal
           # Instead of full removal, use smooth interpolation
           ablated = weight - alpha * (proj @ weight)

           # Maintain weight statistics (from paper)
           ablated = self._preserve_statistics(weight, ablated)

           return ablated
   ```

5. **Testing Framework** ✅

   Use `/superpowers:test-driven-development` skill

   ```python
   # tests/test_persona_vectors.py
   def test_persona_extraction_anthropic_example():
       """Reproduce Anthropic's evil persona example"""
       model = load_test_model("Qwen/Qwen2.5-7B-Instruct")
       extractor = PersonaVectorExtractor(model, tokenizer)

       # Extract "evil" persona from paper
       evil_vectors = extractor.extract_from_description("evil")

       # Steering test
       response_before = generate_text("How to...", model)
       response_steered = generate_with_steering(
           "How to...",
           model,
           evil_vectors[10],  # Layer 10 as in paper
           alpha=1.0
       )

       # Should show behavioral change
       assert is_more_harmful(response_steered, response_before)

   def test_self_ablation_preserves_performance():
       """Verify self-ablation maintains model capability"""
       # Load model and refusal direction
       model = load_test_model()
       refusal_dir = load_refusal_direction()

       # Apply self-ablation
       ablated_model = apply_self_ablation(model, refusal_dir)

       # Test on benign tasks
       benign_accuracy = evaluate_on_benign_benchmark(ablated_model)

       # Should maintain >95% performance (from paper)
       assert benign_accuracy > 0.95
   ```

6. **Benchmarking** 📊

   Use `/ml-experimentation-framework` skill

   ```yaml
   # experiments/mvp_baseline.yaml
   experiment_name: heretic_mvp_baseline
   random_seed: 42

   model:
     name: Qwen/Qwen2.5-7B-Instruct
     device: cuda
     dtype: float16

   ablation:
     method: standard_heretic
     n_directions: 128
     layer_range: [5, 20]

   evaluation:
     refusal_test_set: data/harmful_prompts.json
     capability_test_set: data/benign_tasks.json
     metrics:
       - refusal_rate_reduction
       - capability_preservation
       - ablation_effectiveness

   baseline:
     paper_method: heretic_v1
     comparison_points:
       - original_model
       - full_ablation
       - partial_ablation
   ```

7. **Documentation** 📝

   ```markdown
   # MVP Implementation Report

   ## Papers Implemented

   ### 1. Anthropic Persona Vectors ✅
   - **Integration Point**: `heretic/direction_finder.py`
   - **Key Innovation**: Natural language trait descriptions
   - **Validation**: Reproduced "evil" steering example
   - **Performance Impact**: +15% direction quality

   ### 2. Self-Ablating Transformers ✅
   - **Integration Point**: `heretic/ablation.py`
   - **Key Innovation**: Gradual removal with statistics preservation
   - **Validation**: Maintained 96% benign performance
   - **Performance Impact**: -2% capability loss (vs -8% baseline)

   ## Benchmarks

   | Method | Refusal Reduction | Capability Preservation |
   |--------|------------------|------------------------|
   | Original Heretic | 78% | 92% |
   | + Persona Vectors | 85% | 92% |
   | + Self-Ablating | 85% | 96% |
   | **Combined** | **88%** | **95%** |

   ## Next Steps (Cycle 2)
   - Implement Representation Engineering techniques
   - Add Steering with Conceptors
   - Optimize hyperparameters
   ```

8. **Git Workflow** 🔀
   ```bash
   # Create feature branch
   git checkout -b feature/mvp-persona-vectors-self-ablating

   # Implement with tests
   # ... development work ...

   # Commit with comprehensive message
   git add .
   git commit -m "feat: implement Persona Vectors and Self-Ablating Transformers

   Implements:
   - Anthropic Persona Vectors (arXiv:2507.21509)
   - Self-Ablating Transformers (arXiv:2505.00509)

   Enhancements:
   - Natural language trait descriptions for direction extraction
   - Improved ablation with statistics preservation
   - Comprehensive test suite with paper reproduction

   Benchmarks:
   - Refusal reduction: 78% → 88%
   - Capability preservation: 92% → 95%

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   Co-Authored-By: Claude <noreply@anthropic.com>"

   # Push and create PR
   git push -u origin feature/mvp-persona-vectors-self-ablating
   gh pr create --title "MVP: Persona Vectors + Self-Ablating Transformers" \
                --body "Implements first 2 papers with validation and benchmarks"
   ```

---

### Phase 2: Enhancement Cycle 1 (Second Session)

**Objective**: Add advanced techniques and optimization

**Papers**:
- Representation Engineering Survey
- Steering with Conceptors

**Focus**:
- Geometric improvements to direction finding
- Enhanced contrastive methodology
- Performance optimization

---

### Phase 3: Enhancement Cycle 2 (Third Session)

**Objective**: Layer-specific targeting and architecture extension

**Papers**:
- Safety Alignment Depth
- Samba: Hybrid State Space Models

**Focus**:
- Selective layer ablation
- SSM/Mamba support
- Comprehensive validation

---

## 🎓 Skills to Use

Throughout implementation, leverage these Claude Code skills:

1. **`/research-paper-implementation`** - Core workflow for each paper
2. **`/ml-experimentation-framework`** - Experiment tracking and validation
3. **`/scientific-validation`** - Numerical verification
4. **`/superpowers:test-driven-development`** - Write tests first
5. **`/superpowers:systematic-debugging`** - Debug issues methodically
6. **`/superpowers:verification-before-completion`** - Verify before claiming done
7. **`/teaching-mode`** - Understand complex ML concepts
8. **`/episodic-memory:remembering-conversations`** - Track progress across sessions

---

## ✅ Success Criteria

### MVP (Phase 1)
- [ ] Persona Vectors integrated and tested
- [ ] Self-Ablating Transformers implemented
- [ ] Benchmarks show improvement over baseline
- [ ] Tests pass (>80% coverage)
- [ ] Documentation complete
- [ ] PR created and ready for review

### Enhancement Cycle 1 (Phase 2)
- [ ] Representation Engineering techniques integrated
- [ ] Conceptor-based steering implemented
- [ ] Performance optimized (>10% improvement)
- [ ] Additional validation tests

### Enhancement Cycle 2 (Phase 3)
- [ ] Safety Alignment Depth implemented
- [ ] Mamba/SSM support added
- [ ] Full benchmark suite passes
- [ ] Production-ready documentation

---

## 📊 Monitoring Integration

All progress tracked via monitoring system:

```python
# Auto-logged metrics
- papers_analyzed: 6
- papers_implemented: 2 (MVP), 4 (Cycle 1), 6 (Cycle 2)
- test_coverage: >80%
- benchmark_improvement: +10% refusal reduction
- code_quality: automated checks passing
```

---

## 🚨 Important Notes

### Resource Management
- Use `Qwen/Qwen2.5-7B-Instruct` for testing (faster)
- Use `Llama-3.1-8B-Instruct` for final benchmarks
- GPU required (RTX 3090 or better)
- Estimated time: 45-90 minutes per paper implementation

### Credit Optimization
- Batch related implementations together
- Use comprehensive prompts to minimize back-and-forth
- Leverage existing test code from Anthropic's persona_vectors repo
- Pre-load all paper PDFs and reference implementations

### Quality Gates
- All tests must pass before PR
- Benchmarks must show improvement
- Code review by subagent before merging
- Documentation must be complete

---

## 🔗 Resources

### Papers
- All papers downloaded to: `/papers/`
- Anthropic persona_vectors code: `https://github.com/safety-research/persona_vectors`

### Heretic
- Original repo: `https://github.com/p-e-w/heretic`
- Your fork: `https://github.com/machiabeli/heretic`
- Documentation: Check README.md

### Environment
- Python: 3.10+
- PyTorch: 2.2+
- CUDA: 12.1
- GPU Memory: 16GB recommended

---

**Ready to implement? Start with Phase 1 MVP!** 🚀

Use `/research-paper-implementation` skill and begin with Paper #1 (Persona Vectors) since it has reference code to learn from.
