# -*- coding: utf-8 -*-
#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2020 - Sequana Development Team
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import sys
import os
import argparse
import shutil
import subprocess

from sequana_pipetools.options import *
from sequana_pipetools.misc import Colors
from sequana_pipetools.info import sequana_epilog, sequana_prolog

col = Colors()

NAME = "rnaseq"


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            epilog=epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)

        so = InputOptions()
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)

        pipeline_group = self.add_argument_group("pipeline_general")
        pipeline_group.add_argument("--genome-directory", dest="genome_directory",
            default=".", required=True)
        pipeline_group.add_argument("--aligner", dest="aligner", required=True,
            choices=['bowtie2', 'bowtie1', 'star', "salmon"],
            help= "a mapper in bowtie, bowtie2, star")
        pipeline_group.add_argument("--force-indexing", action="store_true",
            default=False,
            help="""If indexing files exists already, but you wish to
                create them again, use this option. Note that you will need
                permissions for that""")
        pipeline_group.add_argument("--rRNA-feature",
            default="rRNA",
            help="""Feature name corresponding to the rRNA to be identified in
the input GFF/GTF files""")
        pipeline_group.add_argument("--contaminant-file",
            default=None,
            help="""A fasta file. If used, the rRNA-feature cannot be used. 
This option is useful if you have a dedicated list of rRNA feature or a dedicatd 
fasta file to search for contaminants""")

        # cutadapt related
        so = CutadaptOptions()
        so.add_options(self)

        # fastq_screen
        pipeline_group = self.add_argument_group("section_fastq_screen")
        pipeline_group.add_argument("--do-fastq-screen", action="store_true",
            default=False,
            help="do fastq_screen ")
        pipeline_group.add_argument("--fastq-screen-conf",
            default="fastq_screen.conf", type=str,
            help="""a valid fastqc_screen.conf file. See fastq_screen
documentation for details. In a nutshell, add a line for each genome you want to
search for in your input data. Each line is 'DATABASE name path BOWTIE2'. The
path includes the path to the genome + its prefix name. If you have your 
own fastq-screen DB and configuration file, use this option. Otherwise, the 
default sequana_rnaseq conf is used (phiX174 only)""")

        # feature counts related
        so = FeatureCountsOptions()
        so.add_options(self)

        # others
        self.add_argument("--run", default=False, action="store_true",
            help="execute the pipeline directly")

        pipeline_group = self.add_argument_group("pipeline_others")
        pipeline_group.add_argument('--do-igvtools', action="store_true", 
            help="""if set, this will compute TDF files that can be imported in
IGV browser. TDF file allows to quickly visualise the coverage of the mapped
reads.""")
        pipeline_group.add_argument('--do-bam-coverage', action="store_true", 
            help="Similar to --do-igvtools using bigwig")
        pipeline_group.add_argument('--do-mark-duplicates', action="store_true", 
            help="""Mark duplicates. To be used e.g. with QCs""")

        pipeline_group = self.add_argument_group("pipeline_RNAseQC")
        pipeline_group.add_argument('--do-rnaseqc', action="store_true",
            help="do RNA-seq QC using RNAseQC v2")
        pipeline_group.add_argument('--rnaseqc-gtf-file',
            help="""The GTF file to be used for RNAseQC. Without a valid GTF,
            RNAseqQC will not work. Again, yu may try sequana.gff3 module to build the gtf""")

        # RNADIFF
        pipeline_group = self.add_argument_group("section_rnadiff")
        pipeline_group.add_argument('--rnadiff-mode', type=str,
            required=False,
            choices=["one_factor", "GLM"],
            default="one_factor",
            help="""Fix the type of analyis (one_factor or GLM). By default uses one_factor""")

    def parse_args(self, *args):
        args_list = list(*args)
        if "--from-project" in args_list:
            if len(args_list)>2:
                msg = "WARNING [sequana]: With --from-project option, " + \
                        "pipeline and data-related options will be ignored."
                print(col.error(msg))
            for action in self._actions:
                if action.required is True:
                    action.required = False
        options = super(Options, self).parse_args(*args)
        return options


def main(args=None):

    if args is None:
        args = sys.argv

    # whatever needs to be called by all pipeline before the options parsing
    from sequana_pipetools.options import before_pipeline
    before_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])


    from sequana.pipelines_common import SequanaManager

    # the real stuff is here
    manager = SequanaManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()
    from sequana import logger
    logger.level = options.level

    # fill the config file with input parameters
    if options.from_project is None:
        cfg = manager.config.config

        # --------------------------------------------------------- general
        cfg.general.genome_directory = os.path.abspath(options.genome_directory)
        cfg.general.aligner = options.aligner

        # genome name = cfg.genome.genome_directory
        genome_name = cfg.general.genome_directory.rsplit("/", 1)[1]
        prefix= cfg.general.genome_directory 
        fasta = cfg.general.genome_directory + f"/{genome_name}.fa"
        if os.path.exists(fasta) is False:
            logger.critical("""Could not find {}. You must have the genome sequence in fasta with the extension .fa named after the genome directory.""".format(fasta))
            sys.exit()

        # Do we need the indexing ?
        if options.aligner == "bowtie2":
            if os.path.exists(prefix + f"/bowtie2/{genome_name}.rev.1.bt2"):
                logger.info("Indexing found for {}.".format("bowtie2"))
                cfg.general.indexing = False
            else:
                logger.info("Indexing not found for {}. Planned to be run".format("bowtie2"))
                cfg.general.indexing = True
        elif options.aligner == "star":
            if os.path.exists(prefix + f"/star/SAindex"):
                logger.info("Indexing found for {}.".format("STAR"))
                cfg.general.indexing = False
            else:
                logger.info("Indexing not found for {}. Planned to be run".format("STAR"))
                cfg.general.indexing = True
        elif options.aligner == "bowtie1":
            if os.path.exists(prefix + f"/bowtie1/{genome_name}.rev.1.ebwt"):
                logger.info("Indexing found for {}.".format("bowtie1"))
                cfg.general.indexing = False
            else:
                logger.info("Indexing not found for {}. Planned to be run".format("bowtie1"))
                cfg.general.indexing = True
        elif options.aligner == "salmon":
            if os.path.exists(cfg.general.genome_directory + "/salmon/salmon.done"):
                logger.info("Indexing found for {}.".format("salmon"))
                cfg.general.indexing = False
            else:
                logger.info("Indexing not found for {}. Planned to be run".format("salmon"))
                cfg.general.indexing = True

        #options.do_indexing
        cfg.general.force_indexing = options.force_indexing
        cfg.general.rRNA_feature = options.rRNA_feature
        cfg.general.contaminant_file = options.contaminant_file

        if options.rRNA_feature and options.contaminant_file:
            logger.error("--rRNA-feature and --contaminant-file are mutually exclusive")
            sys.exit(1)

        # --------------------------------------------------------- cutadapt
        cfg.cutadapt.do = not options.skip_cutadapt
        manager.update_config(cfg, options, "cutadapt")

        # ----------------------------------------------------  others
        cfg.input_directory = os.path.abspath(options.input_directory)
        cfg.input_pattern = options.input_pattern
        cfg.input_readtag = options.input_readtag

        # ----------------------------------------------------- feature counts
        cfg.feature_counts.options = options.feature_counts_options
        cfg.feature_counts.strandness = options.feature_counts_strandness
        cfg.feature_counts.attribute = options.feature_counts_attribute
        cfg.feature_counts.feature = options.feature_counts_feature_type
        cfg.feature_counts.extra_attributes = options.feature_counts_extra_attributes

        # ------------------------------------------------------ optional
        cfg.igvtools.do = options.do_igvtools
        cfg.coverage.do = options.do_bam_coverage
        cfg.mark_duplicates.do = False
        if options.do_mark_duplicates:
            cfg.mark_duplicates.do = True

        # -------------------------------------------------------- RNAseqQC
        cfg.rnaseqc.do = options.do_rnaseqc
        cfg.rnaseqc.gtf_file = options.rnaseqc_gtf_file

        # -------------------------------------------------------- RNAdiff
        cfg.rnadiff.mode = options.rnadiff_mode

        # ----------------------------------------------------- fastq_screen conf
        # copy the default fastq_screen conf file
        import sequana_pipelines.rnaseq
        shutil.copy(os.path.join(sequana_pipelines.rnaseq.__path__[0] ,
                "fastq_screen.conf"), manager.workdir)
        if options.do_fastq_screen:
            cfg.fastq_screen.do = True
        else:
            cfg.fastq_screen.do = False

        if os.path.exists(options.fastq_screen_conf):
            cfg.fastq_screen.config_file = os.path.abspath(options.fastq_screen_conf)
            # copy the fastq_screen.conf input or default file
            shutil.copy(options.fastq_screen_conf, manager.workdir)


        # SANITY CHECKS
        # -------------------------------------- do we find rRNA feature in the GFF ?
        logger.info("checking your input GFF file and rRNA feature if provided")

        from sequana.gff3 import GFF3
        genome_directory = os.path.abspath(cfg["general"]["genome_directory"])
        genome_name = genome_directory.rsplit("/", 1)[1]
        prefix_name = genome_directory + "/" + genome_name
        gff_file = prefix_name + ".gff"
        gff = GFF3(gff_file)
        df_gff = gff.get_df()
        valid_types = gff.get_types()

        # first check the rRNA feature
        if cfg['general']["rRNA_feature"] and \
            cfg['general']["rRNA_feature"] not in valid_types:

            logger.error("rRNA feature not found in the input GFF ({})".format(gff_file) +
                " This is probably an error. Please check the GFF content and /or"
                " change the feature name with --rRNA-feature based on the content"
                " of your GFF. Valid features are: {}".format(valid_types))
            sys.exit()


        # then, check the main feature
        fc_type = cfg.feature_counts.feature
        fc_attr = cfg.feature_counts.attribute

        logger.info("checking your input GFF file and feature counts options")
        # if only one feature (99% of the projet)
        if "," not in fc_type:
            fc_types = [fc_type]
        else:
            logger.info("Building a custom GFF file (custom.gff) using Sequana. Please wait")
            fc_types = fc_type.split(',')
            gff.save_gff_filtered(features=fc_types, filename='custom.gff')
            cfg.general.custom_gff = 'custom.gff'

        for fc_type in fc_types:
            S = sum(df_gff['type'] == fc_type)
            if S == 0:
                logger.error("Found 0 entries for feature '{}'. Please choose a valid feature from: {}".format(fc_type, valid_types))
                sys.exit()
            else:
                logger.info("Found {} {} entries".format(S, fc_type))

            # now we check the attribute:
            dd = df_gff.query("type==@fc_type")
            attributes = [y for x in dd.attributes for y in x.keys()]
            S = attributes.count(fc_attr)
            if S == 0:
                logger.error("Found 0 entries for attribute '{}'. Please choose a valid attribute from: {}".format(fc_attr, set(attributes)))
                sys.exit()
            else:
                unique = set([x[fc_attr] for k,x in dd.attributes.items() if fc_attr in x])
                logger.info("Found {} {} entries for attribute '{}' [{} unique entries]".format(S,
fc_attr, fc_type, len(unique)))

            if S != len(unique):
                logger.warning("Attribute non-unique. Feature counts should handle it")

            if options.feature_counts_extra_attributes:
                for extra_attr in cfg.feature_counts.extra_attributes.split(","):
                    if extra_attr not in set(attributes):
                        logger.error("{} not found in the GFF attributes. Try one of {}".format(extra_attr, set(attributes)))
                        sys.exit()
            


    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()
    # need to move the custom file into the working directoty
    try: # option added in latest version
        if cfg.general.custom_gff:
            shutil.copy(cfg.general.custom_gff, options.workdir)
    except:
        pass


    if options.run:
        subprocess.Popen(["sh", '{}.sh'.format(NAME)], cwd=options.workdir)



if __name__ == "__main__":
    main()
