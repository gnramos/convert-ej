\NeedsTeXFormat{LaTeX2e}[1999/12/01]%

\ProvidesClass{boca}[2020/05/12 Formatacao de problemas/contests para o juiz eletronico BOCA.]%

\DeclareOption{notes}{\def\notes@boca{1}}%
\DeclareOption{tutorial}{\def\tutorial@boca{1}}%
\ProcessOptions\relax%

\LoadClass[12pt]{article}

\usepackage{catchfile}%
\usepackage{graphicx}%
\usepackage{ifthen}%
\usepackage{pgffor}%
\usepackage[utf8]{inputenc}%
\usepackage{verbatim}%

\newcommand{\@exampleCell}[1]{%
	\vspace{-1.2\baselineskip}%
	\verbatiminput{#1}%
	\vspace*{-2\baselineskip}%
}%

\newcommand{\@iotable}[2]{%
	\noindent%
	\begin{tabular}[t]{|p{.475\textwidth}|p{.475\textwidth}|}%
		\hline%
		#1 & #2 \\\hline%
	\end{tabular}%
}%

% Para cada exemplo, gera uma tabela.
\newcommand{\@tabelasDeExemplos}[1]{%
	\CatchFileEdef{\examplelist}{#1/examples.csv}{\endlinechar=-1}%

	\@iotable{\textbf{Entrada}}{\textbf{Saída}}%

	\foreach \ex in \examplelist {
		\@iotable{\@exampleCell{#1/../input/\ex}}{\@exampleCell{#1/../output/\ex}}%
	}
}%

\newcounter{@problem}%
\newcommand{\problem}[1]{%
	\stepcounter{@problem}%
	\newpage%
	\graphicspath{{#1/}}%

	\begin{center}%
	\large{\textbf{Problema~\Alph{@problem}}}%
	\\%
	\LARGE{\textbf{\input{#1/title}}}%
	\\%
	\footnotesize{Limite de tempo: \input{#1/time_limit}s}%
	\end{center}%

	\input{#1/description}%

	\section*{Entrada}%
	\input{#1/input}%

	\section*{Saída}%
	\input{#1/output}%

	\section*{Exemplos}%
	\@tabelasDeExemplos{#1}%

	\ifcsname notes@boca\endcsname
		\section*{Observações}%
		\input{#1/notes}%
	\fi%

	\ifcsname tutorial@boca\endcsname
		\section*{Tutorial}%
		\input{#1/tutorial}%
	\fi%
}%

\endinput%