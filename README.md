# PatchWeave

Semantic based patch transplantation tool for C programs. PatchWeave transplants patches across programs which are semantically equivalent but syntactically different, to fix bugs/vulnerabilities that exist across multiple programs (i.e. recurring vulnerabilities)

## Docker Image ##

PatchWeave is distributed in source code form and pre-installed in Docker image. The Docker image also contains PatchWeave evaluation results.

You can [download](https://cloud.docker.com/repository/docker/rshariffdeen/patchweave) Docker image with pre-installed PatchWeave. Note that it contains multiple versions with and without the experiment results, use the correct tag for desired version.

## Known issues

The current PatchWeave implementation fails to run on four cases in the PatchWeave 2020 benchmark set: openjpeg-jasper-buffer-overflow, jasper-openjpeg-buffer-overflow, libsndfile-wavpack-shift-overflow and jasper-openjpeg-null-pointer. Note that we report that PatchWeave generate no patch for these defects in our paper. 

The plausible (but incorrect) patch PatchWeave generates for some examples is compiler 
dependent and possibly machine dependent. PatchWeave relies on compiled AST of the two programs, hence machine dependency is unavoidable with current implementation. 

## Citing

If you use PatchWeave in an academic work consider citing:

<details>

<summary>BibTeX</summary>

  ```bibtex
  @article{10.1145/3412376,
  author = {Shariffdeen, Ridwan Salihin and Tan, Shin Hwei and Gao, Mingyuan and Roychoudhury, Abhik},
  title = {Automated Patch Transplantation},
  year = {2021},
  issue_date = {January 2021},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  volume = {30},
  number = {1},
  issn = {1049-331X},
  url = {https://doi.org/10.1145/3412376},
  doi = {10.1145/3412376},
  abstract = {Automated program repair is an emerging area that attempts to patch software errors and vulnerabilities. In this article, we formulate and study a problem related to automated repair, namely automated patch transplantation. A patch for an error in a donor program is automatically adapted and inserted into a “similar” target program. We observe that despite standard procedures for vulnerability disclosures and publishing of patches, many un-patched occurrences remain in the wild. One of the main reasons is the fact that various implementations of the same functionality may exist and, hence, published patches need to be modified and adapted. In this article, we therefore propose and implement a workflow for transplanting patches. Our approach centers on identifying patch insertion points, as well as namespaces translation across programs via symbolic execution. Experimental results to eliminate five classes of errors highlight our ability to fix recurring vulnerabilities across various programs through transplantation. We report that in 20 of 24 fixing tasks involving eight application subjects mostly involving file processing programs, we successfully transplanted the patch and validated the transplantation through differential testing. Since the publication of patches make an un-patched implementation more vulnerable, our proposed techniques should serve a long-standing need in practice.},
  journal = {ACM Trans. Softw. Eng. Methodol.},
  month = dec,
  articleno = {6},
  numpages = {36},
  keywords = {code transplantation, dynamic program analysis, Program repair, patch transplantation}
  }
  ```

</details>
