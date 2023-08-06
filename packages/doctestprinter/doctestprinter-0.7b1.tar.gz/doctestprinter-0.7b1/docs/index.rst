.. isisysvic3daccess documentation master file, created by
   sphinx-quickstart on Fri Sep 25 10:54:55 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================
Documentation of doctestprinter
===============================

**doctestprinter** contains convenience functions to print outputs more adequate
for doctests.

Example features:

- removes trailing whitespaces: pandas.DataFrame generates trailing whitespaces,
  which interferes with auto text 'trailing whitespace' removal features,
  leading to failed tests.
- maximum line width: break long sequences at whitespaces to a paragraph.

.. image:: ../doctestprinter-icon.svg
   :height: 192px
   :width: 192px
   :alt: my_module
   :align: center

Indices and tables
==================

* :ref:`genindex`

Installation
============

Either install the current release from pip ...

.. code-block:: shell

   pip install <my_module>

... or the latest *dev*elopment state of the gitlab repository.

.. code-block:: shell

   $ pip install git+https://<repository_base_url>/<my_module>.git@dev --upgrade


.. autosummary::
   :toctree: api_reference

   doctestprinter.remove_trailing_whitespaces
   doctestprinter.repr_posix_path
   doctestprinter.strip_base_path
   doctestprinter.round_collections
   doctestprinter.prepare_print
   doctestprinter.doctest_print
   doctestprinter.doctest_iter_print
